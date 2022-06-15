import copy
import logging

from ScEpTIC.AST.elements.instructions.memory_operations import LoadOperation, StoreOperation
from ScEpTIC.AST.elements.instructions.other_operations import CallOperation
from ScEpTIC.AST.elements.instructions.termination_instructions import ReturnOperation
from ScEpTIC.AST.register_allocation.linear_scan.register_operations import SaveRegistersOperation
from ScEpTIC.emulator.intermittent_executor.anomalies import MemoryAccessAnomaly
from ScEpTIC.exceptions import ConfigurationException, AnomalyException, MemoryException, StopAnomalyFoundException, StopException

from .base import InterruptionManager


class EvaluateMemoryAnomaliesInterruptionManager(InterruptionManager):
    """
    Interruption manager for evaluating the effects of memory-related intermittence anomalies
    """

    do_data_anomaly_check = True

    def __init__(self, vmstate, checkpoint_manager):
        super().__init__(vmstate, checkpoint_manager)
        
        if checkpoint_manager.stop_on_power_interrupt:
            self.vmstate.execution_depth = 0

        # list of instructions to be ignored for interruption (= anomaly already found on them)
        self.ignore_pc = []

        # if checkpoint placement is dynamic, checkpoints are taken when an interrupt happens.
        self.do_checkpoint_on_power_interrupt = self.checkpoint_manager.checkpoint_placement == 'dynamic'
        self.vmstate.raise_memory_anomaly_exceptions = self.do_checkpoint_on_power_interrupt

        # interrupt before free and realloc (free <-> ralloc anomaly; realloc <-> any memory operation -> anomaly)
        self.heap_write_functions = ['free', 'realloc']

        for i in range(0, len(self.heap_write_functions)):
            self.heap_write_functions[i] = self.vmstate.ir_function_prefix + self.heap_write_functions[i]

        self._init_interrupt_address_space()


    def _init_interrupt_address_space(self):
        """
        Initializes the address spaces to be verified for consistency.
        """

        # address prefixes in which an interrupt is required
        self.interrupt_prefixes = []
        self.interrupt_write_prefix = []
        self.interrupt_heap = False
        self.interrupt_stack = False
        
        # address prefixes
        prefixes = self.vmstate.memory.address_prefixes

        # append elements which are not restored
        if not self.checkpoint_manager.restore_stack:
            self.interrupt_prefixes.append(prefixes['stack'])
            self.interrupt_stack = True

        if not self.checkpoint_manager.restore_heap:
            self.interrupt_prefixes.append(prefixes['heap'])
            self.interrupt_write_prefix.append(prefixes['heap'])
            self.interrupt_heap = True

        if not self.checkpoint_manager.restore_sram_gst:
            self.interrupt_prefixes.append(prefixes['sram_gst'])

        if not self.checkpoint_manager.restore_nvm_gst:
            self.interrupt_prefixes.append(prefixes['nvm_gst'])


    def _consider_address_space(self, address, check_write = False):
        """
        Returns if an address is in the memory section to be considered for anomaly verifications.
        """

        prefix = address.split('-0x')[0] + '-'

        # if write address is taken into account
        if check_write:
            return len(self.interrupt_write_prefix) > 0 and prefix in self.interrupt_write_prefix

        if prefix in self.interrupt_prefixes:
            return True

        return False


    def intermittent_execution_required(self):
        """
        Returns if the current operation requires an intermittent execution.
        """

        if self.vmstate.register_file.pc in self.ignore_pc:
            return False

        current_instruction = self.vmstate.current_instruction
        
        # if static checkpoint mechanism
        if not self.do_checkpoint_on_power_interrupt:

            # test power failures before first checkpoint
            if self.vmstate.global_clock == 0:
                return True

            # if a call operation is going to be run, verify if it is a checkpoint.
            # if it is a checkpoint, skip it (checkpoint done by simulator) and return True
            if isinstance(current_instruction, CallOperation) and current_instruction.name == self.checkpoint_manager.routine_names['checkpoint']:
                # skip checkpoint
                self.vmstate.register_file.pc.increment_pc()
                self.vmstate.global_clock += 1
                return True

            return False

        # Interrupt required before load execution (WAR)
        if isinstance(current_instruction, LoadOperation):
            address = current_instruction.get_load_address()
            return self._consider_address_space(address)

        # Interrupt required before store execution if heap in NVM
        if self.interrupt_heap and isinstance(current_instruction, StoreOperation):
            address = current_instruction.get_store_address()
            return self._consider_address_space(address, True)

        # Interrupt required after CallOperation, which is instruction 0 of a function.
        if self.interrupt_stack and self.vmstate.register_file.pc.instruction_number == 0 and self.vmstate.register_file.pc.function_name != self.vmstate._main_function_name:
            return True
        
        # Interrupt required for CallOperation if heap in NVM.
        if self.interrupt_heap and isinstance(current_instruction, CallOperation):
            return current_instruction.name in self.heap_write_functions

        return False



    def _intermittent_condition(self, target_global_clock, check_program_ended = True):
        """
        Returns if the intermittent execution tast must continue.
        """

        if self.vmstate.program_end_reached and check_program_ended:
            return False

        # if dynamic checkpoint, consider target_global_clock (execution_depth)
        if self.do_checkpoint_on_power_interrupt:
            return self.vmstate.global_clock < target_global_clock

        current_instruction = self.vmstate.current_instruction

        # if static checkpoint, stop only when another checkpoint is reached.
        if isinstance(current_instruction, CallOperation) and current_instruction.name == self.checkpoint_manager.routine_names['checkpoint']:
            return False

        return True


    def run_with_intermittent_execution(self):
        """
        Runs an intermittent execution as an interrupt was generated just before the current instruction.
        In case of a dynamic checkpoint mechanism, it tests all the next #execution_depth operations.
        In case of a static checkpoint mechanism, it tests all the next operations until another checkpoint is reached.
        For static but dynamic checkpoint mechanisms (-> checkpoint statically placed BUT taken only if power is low)
        the analysis is the same as for the static ones: if I take a checkpoint and then some energy restores my buffer, I can get past the execution depth,
        so is required to analyze the interval from a checkpoint to another (-> execution depth = till next checkpoint, as in static case).

        All the instructions are tested incrementally, so to get all the possible combination of machine resets, and so to observe all possible
        anomalies. If a MemoryException happens, the subsequent instructions cannot be tested, so a consistent dump is restored and the execution
        continue in continuous mode.

        Resets are generated on each instruction which writes on a previosuly read memory area which resides in the NVM/NVM.
        To achieve such optimization of resets points:
            - When a load is run:
                - if its address is in the address space to be verified, save it for further comparisons
                - if its address is in the address space to be verified, and is not the one on which the interruption was generated, set a marker for restore_end_execution.

            - When a store is run, if the target address is in the ones saved from the previously executed loads, resets the state and test the execution until such store is executed.
                If an anomaly happens during such testing, it is stored in the vmstate.anomalies list.

        If an operation (different from the first one) which requires intermittent execution testing is run, a marker is set.
        At the end of the intermittent execution, if such marker is set, a consistent dump is restored since further testing is required in the interval, and in order to be able
        to observe all possible anomalies (and not false-positive due to previous anomalies), the state must be restored to a consistent one.

        If heap is stored in NVM/NVM, a reset is required afeter each heap-specific operation: malloc/free/realloc/calloc.
            -> heap memory wasting is not part of my analysis, so I do not track wasting due to re-execution of malloc/calloc.
            
        If stack is stored in NVM/NVM, a reset is required after each function call (due to stack pushes of arguments, registers, ebp, pc).

        When a reset in triggered, the checkpoint is restored and the instructions are executed until the operation which have generated the reset is reached.
        If an anomaly is found, a consistent state is restored and the execution is forced in continuous execution until the operation which have generated
        the reset is reached.
        Then the intermittent executions continues to do so until the interval termination condition is verified (execution depth reached or checkpoint reached).
        """

        logging.info('[InterruptionManager] Running {} in intermittent execution scenario.'.format(self.vmstate.register_file.pc))

        # do checkpoint (and state dump)
        self.checkpoint_manager.do_checkpoint()

        # execution_depth global clock.
        target_global_clock = self.vmstate.global_clock + self.vmstate.execution_depth
        
        # save interrupt pc to check if further interrupts are needed inside the interval considered
        # (-> used to verify if further loads are present)
        interrupt_global_clock = self.vmstate.global_clock
        interrupt_pc = copy.deepcopy(self.vmstate.register_file.pc)

        # it is True if another load to be analyzed is found inside the interval
        restore_at_the_end = False

        # addresses loaded
        loaded_addresses = []

        # global clocks of the resetted operations
        reset_clocks = []

        # run execution_depth opearations and reset
        while self._intermittent_condition(target_global_clock):
            logging.info('[InterruptionManager] Running {} ({})'.format(self.vmstate.register_file.pc, self.vmstate.global_clock))

            current_instruction = self.vmstate.current_instruction
            current_clock = self.vmstate.global_clock
            
            # if load -> update informations
            if isinstance(current_instruction, LoadOperation):
                address = current_instruction.get_load_address()

                # if the load is in the address space to be verified, populate the loaded_addresses
                if self._consider_address_space(address):
                    loaded_addresses.append(address)

                # if the load is not the one on which the interruption was generated on, and requires an interrupt
                # set the restore_at_the_end to True
                if interrupt_pc != self.vmstate.register_file.pc and self.intermittent_execution_required():
                    restore_at_the_end = True

            # run the actual operation
            self.vmstate.run_step()
            
            do_reset = False
            
            # if store -> verify for reset
            if isinstance(current_instruction, StoreOperation):
                # if store target address is the one of previously saved loads (WAR)
                address = current_instruction.get_store_address()
                do_reset = address in loaded_addresses

            # if heap, the following pairs must be interrupted:
            # LOAD/STORE; LOAD/FREE; LOAD/REALLOC; STORE/FREE; STORE/REALLOC; REALLOC/MALLOC;
            elif self.interrupt_heap and isinstance(current_instruction, CallOperation):
                do_reset = current_instruction.name in self.heap_write_functions or current_instruction.name in [self.vmstate.ir_function_prefix + 'malloc', self.vmstate.ir_function_prefix + 'calloc']
                
                # If reset required, run the heap function and return from it. Then reset.
                if do_reset:
                    # run until the heap instruction can return
                    while not isinstance(self.vmstate.current_instruction, ReturnOperation) and self._intermittent_condition(target_global_clock):
                        self.vmstate.run_step()

                    # run return step
                    if isinstance(self.vmstate.current_instruction, ReturnOperation) and self._intermittent_condition(target_global_clock, False):
                        self.vmstate.run_step()

                    # heap may be modified with REALLOC/FREE/MALLOC, so restore dump at the end
                    restore_at_the_end = True

            # if call and stack in NVM -> reset.
            elif self.interrupt_stack and isinstance(current_instruction, CallOperation):
                do_reset = True

            # if instruction must be resetted and no reset was generated on the instruction
            if do_reset and current_clock not in reset_clocks:
                logging.info('[InterruptionManager] Reset!')

                # append current_clock to ignore resets on this operation.
                reset_clocks.append(current_clock)

                # get current program counter
                current_clock = self.vmstate.global_clock
                reset_pc = copy.deepcopy(self.vmstate.register_file.pc)

                # reset and restore a previously-taken checkpoint
                self.vmstate.reset()
                self.checkpoint_manager.do_restore()

                # verify stack anomaly (after a call -> reset -> if stack differs -> anomaly)
                if self.interrupt_stack:
                    stack_anomalous = self.has_stack_activation_record_anomalies(reset_pc)
                
                    if stack_anomalous:
                        self.ignore_pc.append(interrupt_pc)
                        restore_at_the_end = True
                        break

                # execute operations until current operation and check for anomalies
                try:
                    self._test_run(current_clock, loaded_addresses, reset_pc)

                # if memory exception: a LOAD/FREE STORE/FREE LOAD/REALLOC STORE/REALLOC REALLOC/REALLOC pair was executed.
                # except MemoryException as e: <- not sufficient
                # vm error -> anomaly which would stop execution
                except (StopAnomalyFoundException, StopException):
                    raise

                except Exception as e:

                    anomaly = MemoryAccessAnomaly(reset_pc, current_clock, self.vmstate.register_file.pc, self.vmstate.global_clock, interrupt_pc, e)

                    if anomaly not in self.vmstate.anomalies:
                        self.vmstate.anomalies.append(anomaly)
                        
                        # stats
                        self.vmstate.stats.anomaly_found()
                        
                        self.vmstate.handle_stop_request(anomaly)

                    self.ignore_pc.append(interrupt_pc)

                    restore_at_the_end = True
                    break

        # Adjustment for execution_depth when is 0 (case: stop on checkpoint)
        if self.vmstate.execution_depth == 0:
            self.vmstate.run_step()

        # further analysis is needed inside the considered interval, so restore a consistent state
        # and run until the interrupt global clock is reached
        if restore_at_the_end or self.vmstate.trigger_reset_and_restore:
            logging.info('[InterruptionManager] Dump restored!')

            # restore dump
            self.checkpoint_manager.restore_dump()

            # restore trigger value
            self.vmstate.trigger_reset_and_restore = False

            # if dynamic checkpoint mechanism, run until interrupt global clock is reached
            if self.do_checkpoint_on_power_interrupt:
                while self.vmstate.global_clock <= interrupt_global_clock:
                    self.vmstate.run_step()


    def _test_run(self, target_global_clock, loaded_addresses, reset_pc):
        """
        Runs a series of instructions after an interrupt, until a target global clock is reached.
        If an anomaly is found, it restores an available memory dump (consistent state).
        """

        try:
            # anomalies may be present in any of runned operations after the interrupt, so is required to run them to verify their correctness.
            while self._intermittent_condition(target_global_clock):
                logging.info('[InterruptionManager] Testing run of {} ({})'.format(self.vmstate.register_file.pc, self.vmstate.global_clock))

                self.vmstate.run_step()

        except AnomalyException:
            logging.info('[InterruptionManager] Restoring state!')

            # revert back to consistent state
            self.checkpoint_manager.restore_dump()
            
            # append pc to ignore_pc. NB: it is important to ignore the one restored by the dump:
            # 1: LOAD a
            # 2: LOAD b
            # 3: STORE b, ...
            # 4: STORE a, ...
            # With an execution depth of 3, op.1 won't generate any anomaly, but op.2 will.
            # The problem here is that it will generate the anomaly during the test for op.1, and the
            # simulator will be stuck retrying op.1. Also, if an anomaly would be possible on op.1, it will be
            # considered before the anomaly of op.2 (as the program is tested in-order).
            # So by ignoring the program counter restored by the anomaly, the test will continue.
            # NB: I can't ignore here the PC of op.2, since it would lead to a lack of testing in its interruption boundaries.
            pc = copy.deepcopy(self.vmstate.register_file.pc)

            if pc not in self.ignore_pc:
                self.ignore_pc.append(pc)

            # reset loaded addresses, to avoid unwanted interrupts (e.g. STORE a, LOAD a would generate an interrupt)
            loaded_addresses.clear()

        # If an anomaly is found, restore dump and continue execution until resetting point is reached
        # (the series of runs is executed by the run_with_intermittent_execution main cycle)
        # This part is needed to grant a correct analysis: if no restore_dump is performed and an anomaly is found, the
        # data used for subsequent analysis will contain an anomaly, so some non-real false-positive would be generated
        # and also future branches will be analyzed considering an anomalous state, possibly leading to a wrong analysis.
        if self.vmstate.trigger_reset_and_restore:
            logging.info('[InterruptionManager] Restoring state!')

            self.vmstate.trigger_reset_and_restore = False
            self.checkpoint_manager.restore_dump()

            loaded_addresses.clear()
