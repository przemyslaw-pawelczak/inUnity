import copy

from ScEpTIC.AST.elements.instruction import Instruction
from ScEpTIC.exceptions import MemoryException

class SaveRegistersOperation(Instruction):
    """
    Operation that emulates the saving of registers before a function call.
    All the register savings are done as caller-save, since saving register in the callee
    function will lead to multiple SaveRegistersOperation (one before each return).
    The instruction is set up with:
        - tick_count: consists in the number of registers used by the called function.
            In a real scenario, 1 store operation (Rx -> stack) will be inserted for each register
            that needs to be saved. Once this instruction is executed, the global clock will be incremented
            by this value ( = number of store operations that should be present)
        - target_reg: is the name of the register that will contain the return value of the call. It won't be restored, nor saved.

    NB: all registers are saved from R0 to R_n, so it is sufficient to provide the number of registers to be saved
    to save the first n registers.
    """

    def __init__(self, tick_count, target_reg, register_pool):
        target_reg_id = register_pool._get_id_from_reg_name(target_reg)

        if target_reg_id is None:
            target_reg_id = tick_count

        """
        Tick count corresponds to the number of registers to be saved, which
        can be converted as a R_i with i in [0, tick_count)
        If the target register is inside such range, tick_count should be decreased by 1
        since the target register will be replaced by the function call and won't be restored
        (it will contain the call's return value)
        """
        if target_reg_id < tick_count:
            tick_count -= 1

        self.tick_count = tick_count
        self.target_reg = target_reg
        super().__init__()
        self._omit_target = True


    def get_val(self):
        """
        Save all registers, except for the target one.
        They will be restored by RestoreRegistersOperation.
        Since saving all registers or a sub-group of them won't change anything,
        this function saves all of them in order to remove a control of which register
        needs to be saved. The overall result is the same as it only some registers are saved,
        since registers computed inside a function won't have any value needed by the caller,
        except from the return register.
        """

        # variables used to store registers
        registers = {}
        registers_input_lookup = {}

        for reg in self._vmstate.register_file._registers:
            if reg != self.target_reg:
                reg = self._vmstate.register_file._registers[reg]
                
                # save register's value
                registers[reg.name] = copy.deepcopy(reg.value)

                # save register's input lookup information
                if self._vmstate.input_lookup_enabled:
                    input_lookup = copy.deepcopy(self._vmstate.register_file.get_input_lookup(reg.name))
                    if input_lookup is not None:
                        registers_input_lookup[reg.name] = input_lookup

        # simulate register saving.
        for _ in range(0, self.tick_count):
            
            if self._vmstate.do_data_anomaly_check:
                self._vmstate.function_call_lookup['regs'].append(self._vmstate.memory.stack.top_address)

            self._vmstate.memory.stack.push(self._vmstate.memory.address_dimension, copy.deepcopy(registers), 'register')

        # save registers into saving_pool
        to_save = {'registers': registers, 'registers_input_lookup': registers_input_lookup}
        self._vmstate.reg_saving_pool.append(to_save)


    def __str__(self):
        return 'SaveRegistersOperation(~{}) [{} ops]'.format(self.target_reg, self.tick_count)


class RestoreRegistersOperation(Instruction):
    """
    Represents an operation that emulates the restoring of registers after a called function returns.
    It is setup by proiding the corresponding SaveRegistersOperation, from which takes the tick_count and the
    registers values to be restored.
    """
    
    def __init__(self, save_registers_operation):
        self.tick_count = save_registers_operation.tick_count
        super().__init__()
        self._omit_target = True


    def get_val(self):
        to_restore = self._vmstate.reg_saving_pool.pop()
        
        # restore each register saved by the SaveRegistersOperation
        # NB: the target register is not included here by construction of the
        # SaveRegistersOperation method.
        for reg in to_restore['registers']:
            self._vmstate.register_file.write(reg, copy.deepcopy(to_restore['registers'][reg]))

        # restore input lookup information.
        if self._vmstate.input_lookup_enabled:
            for reg in to_restore['registers_input_lookup']:
                self._vmstate.register_file._input_lookup[reg] = copy.deepcopy(to_restore['registers_input_lookup'][reg])

        # simulate registers restoring.
        for _ in range(0, self.tick_count):
            stacked_reg_file = self._vmstate.memory.stack.pop(self._vmstate.memory.address_dimension)

            if to_restore['registers'] != stacked_reg_file:
                raise MemoryException('[RestoreRegistersOperation] Register file saved in stack is anomalous (wrong register values).')


    def __str__(self):
        return 'RestoreRegistersOperation() [{} ops]'.format(self.tick_count)
