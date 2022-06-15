import copy
import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements import value
from ScEpTIC.AST.elements.instructions import memory_operations
from ScEpTIC.AST.elements.instructions import other_operations
from ScEpTIC.exceptions import RegAllocException
from ScEpTIC.llvmir_parser.sections_parser import global_vars

from .register_operations import SaveRegistersOperation, RestoreRegistersOperation
from .register_pool import RegisterPool


class LinearScanRegisterAllocator:
    """
    Implementation of linear scan register allocation.
    It must be done for each function and this class refers to a single function body.
    Implementation details can be found here:
    https://www2.seas.gwu.edu/~hchoi/teaching/cs160d/linearscan.pdf
    """

    def __init__(self, function, regs_number, reg_prefix = 'R', spill_prefix = '%spill_', spill_type = 'i32'):
        self.function = function
        self.code = function.body
        
        self.virtual_regs = {}
        self.intervals = []
        
        self.active = []
        
        self.register_pool = RegisterPool(regs_number, reg_prefix)
        
        # prefix of spill registers
        self.spill_prefix = spill_prefix
        self.spill_count = 0
        self.spill_dimension = global_vars.parse_type(spill_type)
        self.reg_count = 0

        # registers to be ignored due to data layout
        self.ignores = []

        # identifies the line of the last alloca
        # it is used to put alloca operations in the same area of the code, as they are translated with a single ESP increment.
        self.last_alloca = 0

        # calculate latest alloca operation
        for i in range(0, len(self.code)):
            self.last_alloca = i
            if not isinstance(self.code[i], memory_operations.AllocaOperation):
                break


    def run_register_allocation(self):
        """
        Runs the actual register allocation.
        """

        self.do_call_pre_processing()
        self.do_liveness_analysis()
        self.do_register_allocation()


    @property
    def spill_type(self):
        """
        Returns an instance of the spill type, to be used in the operations.
        """

        return copy.deepcopy(self.spill_dimension)


    def _name_to_virtual_reg(self, name):
        """
        Returns a Value representing a virtual register with the provided name
        """

        return value.Value('virtual_reg', name, None)


    def _create_virtual_reg(self):
        """
        Creates a new virtual register.
        """

        name = '{}{}'.format(self.spill_prefix, self.spill_count)
        self.spill_count += 1
        logging.debug('[RegisterAllocation] Creating new virtual register {}.'.format(name))
        return self._name_to_virtual_reg(name)


    def append_alloca_operation(self, alloca_type):
        """
        Appends an alloca operation in the code at the end of the alloca section.
        It returns the virtual registers contining the alloca address.
        """
        logging.debug('[RegisterAllocation] Appending alloca({}) operation on top.'.format(len(alloca_type)))

        spill_reg = self._create_virtual_reg()
        target = copy.deepcopy(spill_reg)

        # create the operation
        alloca = memory_operations.AllocaOperation(target, alloca_type, 1, 1)
        
        # insert it in the code
        self.code.insert(self.last_alloca, alloca)
        
        # update last_alloca, so to consider this added one.
        self.last_alloca += 1

        return spill_reg


    def append_store_operation(self, position, target, value, target_type, label, metadata):
        """
        Appends a store operation at the required position.
        """

        logging.debug('[RegisterAllocation] Appending store {}, {} at {}.'.format(target.value, value.value, position))

        target = copy.deepcopy(target)
        value = copy.deepcopy(value)
        
        value.type = copy.deepcopy(target_type)

        # create the operation
        store = memory_operations.StoreOperation(target, value, 1, False)
        store.label = label
        store.metadata = metadata

        # insert in the code the operation
        self.code.insert(position, store)


    def append_load_operation(self, position, element, load_type, is_arg_of_function_call, metadata):
        """
        Appends a load operation at the required position.
        It returns the virtual register containing the loaded value.
        """

        logging.debug('[RegisterAllocation] Appending load {} at {}.'.format(element.value, position))
        
        spill_reg = self._create_virtual_reg()
        target = copy.deepcopy(spill_reg)
        element = copy.deepcopy(element)

        # create the operation
        load = memory_operations.LoadOperation(target, load_type, element, 1, False)
        load.metadata = metadata
        
        # eventually set if it loads a function call's argument
        if is_arg_of_function_call:
            load.is_arg_of_function_call = True
        
        # insert in the code the operation
        self.code.insert(position, load)

        return spill_reg


    def do_call_pre_processing(self):
        """
        Applies call pre-processing, consisting in:
            - marking load of arguments as is_arg_of_function_call
            - creating alloca-store-load for immediate
            - creating alloca-store-load for conversion and other operation s.t. their
                results are passed as arguments of the function call.
        """

        search_from = 0
        search_to = 0
        i = 0
        
        # scan the code by line. while is used since the lines number may change
        while i < len(self.code):
            operation = self.code[i]

            # process only call operations which are not part of the checkpoint mechanism.
            if isinstance(operation, other_operations.CallOperation) and operation.name in self.function._calls:
                targets = operation.get_uses()
                search_to = i
                j = search_from

                # adjust label (if present)
                append_label = operation.label
                
                # search for instructions s.t. their target is in function arguments
                while j < search_to:
                    op = self.code[j]

                    # target of operation is an argument of the call
                    if 'target' in op.__dict__ and op.target is not None and op.target.value in targets:
                            targets.remove(op.target.value)

                            # if is a load instruction, mark it
                            if isinstance(op, memory_operations.LoadOperation):
                                op.is_arg_of_function_call = True
                            # else generate alloca, store and load, as it would be done
                            # in a real scenario (value saved onto the stack to be passed)
                            # NB: load is marked as is_arg_of_function_call (so to emulate stack passing)
                            
                            else:
                                # get type of argument
                                arg_type = operation.get_type_from_virtual_reg(op.target.value)
                                
                                # append alloca and compensate for the added instruction
                                tmp_reg = self.append_alloca_operation(arg_type)

                                # append store before call and compensate for the added instruction
                                # search_to = call position
                                # nb: here is set the eventual label of the call operation.
                                self.append_store_operation(search_to+1, tmp_reg, op.target, arg_type, append_label, operation.metadata)

                                # set the lable to be appended to None
                                append_label = None
                                
                                # append load before call and compensate for the added instruction
                                tmp_reg = self.append_load_operation(search_to+2, tmp_reg, arg_type, True, operation.metadata)
                                
                                # update the new register name containing the argument value.
                                operation.replace_reg_name(op.target.value, tmp_reg.value)
                                
                                # compensate for the 3 added instructions
                                i += 3

                                # update search_to value, to consider added instructions
                                search_to = i

                    # update code index
                    j += 1

                # create alloca, store and load for immediate values, as it is done
                # for operations on the above lines.
                
                for arg in operation.function_args:
                    if arg.value_class == 'immediate':
                        
                        # llvm builtins may have 1bit operations, but memory can only work
                        # with bytes, so modify the memory dimension to do not have problems.
                        # data integrity is preserved.
                        if arg.type is not None and arg.type.base_type.bits < 8:
                            arg.type.base_type.bits = 8
                        
                        tmp_reg = self.append_alloca_operation(arg.type)
                        i += 1

                        # nb: here is set the eventual label of the call operation.
                        self.append_store_operation(i, tmp_reg, arg, arg.type, append_label, operation.metadata)
                        # set the lable to be appended to None
                        append_label = None
                        i += 1
                        
                        tmp_reg = self.append_load_operation(i, tmp_reg, arg.type, True, operation.metadata)
                        i += 1
                        
                        # update the arguments to be a virtual register instead of an immediate
                        arg.value_class = 'virtual_reg'

                        # set the virutal register name
                        arg.value = tmp_reg.value
                
                # update search from. it is used to limit the area in which function arguments are searched.
                # in llvm all arguments are reloaded if multiple calls happens from them, so there is no need
                # to search arguments from the top (it is sufficient to go from the previous call to the current one)
                search_from = i + 1

                # refresh the operation label: if it is assigned to another operation, it will be set to false
                # otherwise is unchanged.
                operation.label = append_label

            # update code index
            i += 1


    def do_call_post_processing(self):
        """
        Applies function call post-processing, which consists in:
            - Insertion of SaveRegistersOperation and RestoreRegistersOperation respectively before and after
                a function call
            - Updating the labels mappings (if code is appended, a label is mapped with a line which won't be exact)
        """

        i = 0

        # scan the code by line. while is used since the lines number may change
        while i < len(self.code):
            operation = self.code[i]

            # process only call operations which are not part of the checkpoint mechanism.
            if isinstance(operation, other_operations.CallOperation) and operation.name in self.function._calls:
                
                # if recursive call, save used registers
                if operation.name == self.function.name:
                    tick_count = self.function.reg_count

                # else estimates the number of registers to be saved in case of a well-partitioned
                # register allocation among functions.
                # e.g. if main uses 2 registers and calls pow which uses 2 registers, a well-partitioned
                # register allocation will give R0 and R1 to main, and R2 and R3 to pow
                # with the result of no register saving needed
                else:
                    # usage = reg used by current function + max reg used by the called function (and calls inside it)
                    # registers to be saved = usage - available
                    # if I have 10 registers, the function uses 2 registers and the called one uses 2 registers,
                    # no saving needed.
                    # max_reg_usage is calculated iteratively before running do_call_post_processing
                    tick_count = self.function.reg_count + operation.get_function_max_reg_usage() - self.register_pool.regs_number

                # if result is < 0 means that no register should be saved.
                if tick_count < 0:
                    tick_count = 0
                
                # get target register name
                if 'target' in operation.__dict__ and operation.target is not None:
                    target = operation.target.get_uses()[0]
                else:
                    target = None

                # create the saving and restoring operations
                save_reg_op = SaveRegistersOperation(tick_count, target, self.register_pool)
                save_reg_op.metadata = operation.metadata

                # compensate label
                save_reg_op.label = operation.label
                operation.label = None

                load_reg_op = RestoreRegistersOperation(save_reg_op)
                load_reg_op.metadata = operation.metadata
                
                # insert the save operation before the function call
                self.code.insert(i, save_reg_op)
                
                # 1 for compensating save_reg_op, 1 for finding the operation after the call
                i += 2
                
                # insert the restore operation after the function call
                self.code.insert(i, load_reg_op)

            i += 1

        # update the function's label mappings.
        self.function.update_labels()
        

    def _init_intervals(self):
        """
        Inits the intervals used for calculating the active interva of the registers for the linear scan.
        """

        for _ in range(0, len(self.code)):
            self.intervals.append(None)


    def do_liveness_analysis(self):
        """
        This method performs the liveness analysis, which finds the live interval for each register.
        NB: LLVM IR is in Static Single Assignment (SSA) foarm, so for obtaining the liveness intervals
        is sufficient to map the definition with its last use.
        """
        # registers to be ignored, since will be considered as stack offsets/addresses
        # which will be resolved by datalayout operation.
        self.ignores = self.function.get_ignore()

        # for each line, compute the uses and definitions of each register.
        for i in range(0, len(self.code)):
            self.ignores = self.ignores + self.code[i].get_ignore()
            defs = tools.list_sanitize_from_list(self.code[i].get_defs(), self.ignores)
            uses = tools.list_sanitize_from_list(self.code[i].get_uses(), self.ignores)

            for reg in defs:
                self.virtual_regs[reg] = {'uses': [], 'def': i, 'target': None}

            for reg in uses:
                self.virtual_regs[reg]['uses'].append(i)

        self._init_intervals()

        # find last use of each register and create interval dict
        for reg_id, reg in self.virtual_regs.items():
            # if no use, the last use will be in the same instruction in which the register
            # is defined
            if len(reg['uses']) == 0:
                reg['uses'].append(reg['def'])
            
            reg['last_use'] = max(reg['uses'])

            # set register intervals
            self.intervals[reg['def']] = {'reg': reg_id, 'last_use': reg['last_use']}


    def _compensate_for_alloca(self):
        """
        Updates the liveness analysis to account for the insertion of an alloca operations.
        """

        logging.debug('[RegisterAllocation] Compensating for alloca operation.')
        
        # alloca operations do not introduces any use/def and are appended on the top of the code
        # so i can insert a None interval on top of the list (since all alloca operations are in the same region)
        self.intervals.insert(0, None)

        # increment uses of each interval by 1
        for interval in self.intervals:
            if interval is None:
                continue

            interval['last_use'] += 1

        # increament uses and definitions of each virtual register by one
        for virtual_reg in self.virtual_regs.values():
            virtual_reg['def'] += 1
            virtual_reg['uses'] = [x+1 for x in virtual_reg['uses']]
            virtual_reg['last_use'] += 1


    def _compensate_for_operation(self, instant):
        """
        Updates the liveness analysis to account for the insertion of an operation which may
        insert use/def and is inserted in a precise line of code.
        instant specifies also the line of code
        """
        logging.debug('[RegisterAllocation] Compensating for operation at {}.'.format(instant))
        
        # insert the proper interval
        self.intervals.insert(instant, None)

        # increment data by 1 for subsequent intervals
        for interval in self.intervals:
            if interval is None:
                continue

            # if subsequent interval, it needs to be updated
            if interval['last_use'] >= instant:
                interval['last_use'] += 1

                # get corresponding virtual register
                virtual_reg = self.virtual_regs[interval['reg']]

                # increment its definition instant if happens after the given instant
                if virtual_reg['def'] >= instant:
                    virtual_reg['def'] += 1

                # increment all the uses by 1 if they are after the given instant
                virtual_reg['uses'] = [x+1 if x >= instant else x for x in virtual_reg['uses']]
                # increment last use by 1, since it will be certainly after the given instant
                virtual_reg['last_use'] += 1


    def _assign_register(self, instant, new_reg_name):
        """
        Assigns a physical register to a virtual register which is defined in a given instant.
        """

        interval = self.intervals[instant]
        reg_name = interval['reg']
        logging.debug('[RegisterAllocation] Assigning register {} to virtual register {} at {}.'.format(new_reg_name, reg_name, instant))
        
        # update each occurrence of the old register with the new register
        for line in self.virtual_regs[reg_name]['uses']:
            self.code[line].replace_reg_name(reg_name, new_reg_name)

        self.code[instant].replace_reg_name(reg_name, new_reg_name)
        self.virtual_regs[reg_name]['target'] = new_reg_name

        # insert register into the active ones.
        self.active.append(interval['reg'])

    def do_register_allocation(self):
        """
        Performs the linear scan register allocation over the given function.
        """

        instant = 0

        # scan all intervals and insert register spills / promotions
        while instant < len(self.intervals):
            interval = self.intervals[instant]

            if interval is None:
                instant += 1
                continue

            # expire old registers
            self.expire_old(instant)

            # set max reg count (used to estimate the tick_count)
            self.reg_count = max(self.reg_count, len(self.active))

            # if all registers used, need to spill.
            if len(self.active) == self.register_pool.regs_number:
                # spill at current instant
                self.spill_at(instant)
                # compensate for alloca and store
                instant += 2

            # else assign register
            else:
                new_reg_name = self.register_pool.get_reg()
                self._assign_register(instant, new_reg_name)

            # increment instant index
            instant += 1

        # set function regiser count.
        self.function.reg_count = self.reg_count


    def expire_old(self, instant):
        """
        Updates the active registers by removing expired ones.
        """

        logging.debug('[RegisterAllocation] Expiring registers at {}.'.format(instant))

        # scan active registers to find if some of them can be freed.
        for reg in self.active:

            # if the last use is before current instant, the register can be
            # considered as free.
            if self.virtual_regs[reg]['last_use'] < instant:

                # remove from active registers
                self.active.remove(reg)

                # free register
                reg_name = self.virtual_regs[reg]['target']
                self.register_pool.free_reg(reg_name)

    def _get_fist_use_after_instant(self, reg, instant):
        """
        Returns the first use of a register after a given instant.
        """

        uses = self.virtual_regs[reg]['uses']
        first_use = self.virtual_regs[reg]['last_use']

        for i in uses:
            if instant < i < first_use:
                first_use = i

        return first_use

    def spill_at(self, instant):
        """
        Selects a register to be spilled in the given instant and spills it.
        """

        selected_spill = None
        selected_reg = None
        latest_use = -1

        # scans each active register.
        for reg in self.active:
            reg_data = self.virtual_regs[reg]

            # if register can be spilled (= not used in this instant nor defined)
            if instant not in reg_data['uses'] and instant != reg_data['def']:
                # get first use after current instant
                first_use = self._get_fist_use_after_instant(reg, instant)

                # update max usage informations, used for spilling selection
                if first_use > latest_use:
                    selected_spill = reg_data['target']
                    selected_reg = reg
                    latest_use = first_use

        # no register can be spilled, exit.
        if selected_spill is None:
            raise RegAllocException('Unable to select a register for spilling')

        logging.debug('[RegisterAllocation] Spilling register {} at instant {}'.format(selected_spill, instant))

        # append alloca operation, to account for stack space
        tmp_reg = self.append_alloca_operation(self.spill_type)
        
        # compensate for alloca
        self._compensate_for_alloca()
        instant += 1
        
        # save register value onto the stack before current instant
        value_reg = self._name_to_virtual_reg(selected_spill)
        self.append_store_operation(instant, tmp_reg, value_reg, self.spill_type, None, self.code[instant].metadata)

        # compensate for store
        self._compensate_for_operation(instant)
        instant += 1

        # compensate for alloca and store. NB: use is after alloca and store
        latest_use += 2
        # create load before the first use of spilled register and
        tmp_reg = self.append_load_operation(latest_use, tmp_reg, self.spill_type, False, self.code[instant].metadata)
        self._compensate_for_operation(latest_use)

        # retarget uses of spilled register to created load (new reg name, which for now is virtual and in
        # a next step will be updated with a physical one)
        uses = [x for x in self.virtual_regs[selected_reg]['uses'] if x >= latest_use]
        for i in uses:
            self.code[i].replace_reg_name(selected_spill, tmp_reg.value)

        # create interval and register for load, so to assign a physical register to it in a next iteration.
        reg_id = tmp_reg.value
        last_use = max(uses)
        virtual_reg = {'uses': uses, 'def': latest_use, 'target': None, 'last_use': last_use}
        self.virtual_regs[reg_id] = virtual_reg
        self.intervals[latest_use] = {'reg': reg_id, 'last_use': last_use}

        # assign register
        self.active.remove(selected_reg)
        self._assign_register(instant, selected_spill)
