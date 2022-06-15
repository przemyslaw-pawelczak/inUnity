from .register_file import RegisterFile

class VirtualRegisterFile(RegisterFile):
    """
    Implementation of a RegisterFile which uses virtual registers.
    In this case, registers are allocated on-the-fly and on function call they are saved.
    """

    requires_register_allocation = False

    # very big number
    param_regs_count = 1000

    def _get_register(self, register_name, operation):
        """
        Returns a register.
        """

        # on write: if register not present, create it.
        if operation == 'write' and register_name not in self._registers:
            self._create_register(register_name)
        
        return super()._get_register(register_name, operation)
    

    def on_function_call(self):
        """
        Callback for function call.
        """

        # Each function has its own virtual registers, which all starts from %0.
        # So I must save them before execution of a function and restore them after its return.
        self._reg_stack.append(self._registers)
        self._registers = {}

        # Update accordingly to the virtual register file behaviour the input lookup information
        self._reg_stack.append(self._input_lookup)
        self._input_lookup = {}

        # set first basic block as latest
        self._reg_stack.append(self.last_basic_block)
        self.last_basic_block = '%0'


    def on_function_return(self):
        """
        Callback for function return.
        """

        self.last_basic_block = self._reg_stack.pop()
        self._input_lookup = self._reg_stack.pop()
        self._registers = self._reg_stack.pop()
