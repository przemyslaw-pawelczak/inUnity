import copy
import logging

from ScEpTIC.exceptions import RegisterFileException

from .register_file import RegisterFile
from .register import Register

class PhysicalRegisterFile(RegisterFile):
    """
    Implementation of a RegisterFile which uses physical registers.
    In this case, registers are pre-allocated but virtual addresses returned by alloca are still present
    and thus are managed with the self._addresses dictionary.
    On function call only _addresses values are saved.
    """

    requires_register_allocation = True

    def __init__(self, register_file_configuration):
        physical_registers_number = register_file_configuration['physical_registers_number']
        
        # register allocator configurations
        self.reg_prefix = register_file_configuration['physical_registers_prefix']
        self.spill_prefix = register_file_configuration['spill_virtual_registers_prefix']
        self.spill_type = register_file_configuration['spill_virtual_registers_type']
        
        # stuff for dynamic loading of the register allocator
        self.allocation_module_prefix = register_file_configuration['allocator_module_location']
        self.allocation_module = register_file_configuration['allocator_module_name']
        self.allocation_function = register_file_configuration['allocator_function_name']
        self.param_regs_count = register_file_configuration['param_regs_count']
        
        # see comment of RegisterFile.write_address(), which explain why this variable is here.
        self._addresses = {}

        # lookup table for input information
        self._address_input_lookup = {}

        # initialize register file
        super().__init__()

        if physical_registers_number < 1:
            raise RegisterFileException('[{}] Register number not valid. It must be higher than 0, {} given.'.format(self.reg_type, physical_registers_number))

        # initialize registers
        for i in range(0, physical_registers_number):
            register_name = '{}{}'.format(self.reg_prefix, i)
            self._create_register(register_name)


    def __eq__(self, other):
        if not isinstance(other, PhysicalRegisterFile):
            return False

        return self._addresses == other._addresses and self._address_input_lookup == other._address_input_lookup and super().__eq__(other)


    def get_visual_dump(self):
        """
        Returns a string representing the memory
        """

        dump = super().get_visual_dump()+"\n\n"

        for i in sorted(self._addresses.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 0):
            dump += str(i)+': '+str(self._addresses[i])+"\n"

        return dump

    def _get_register(self, register_name, operation):
        """
        Returns a register.
        """

        # Makes address_registers transparent.
        # NB: address register can be created only with its own write_address method.
        if operation == 'read' and register_name in self._addresses:
            return Register.direct(register_name, self.read_address(register_name))
        
        return super()._get_register(register_name, operation)


    def write_address(self, register_name, address):
        """
        Set the value of an address register.
        Address are considered only as values returned by alloca operations.
        There are different behaviours depending on physical/virtual register file.
        On physical register file, register allocation is performed.
        Alloca operations just make space on stack and their value is known compile-time.
        This means that the virtual register wouldn't be mapped to a real one, since the stack
        offset is found and directly placed on the load/store operation that uses this portion of memory.
        Also, multiple alloca operations will be mapped to a single increment of the stack.
        (This is done in data layout)
        NB: this is to do not have register's spill due to not doing data layout. In a "real" machine code, those spills won't be there
        """

        self._addresses[register_name] = address
        
        # remove input lookup on write.
        if register_name in self._input_lookup:
            del self._input_lookup[register_name]
        
        if register_name in self._address_input_lookup:
            del self._address_input_lookup[register_name]
            

    def read_address(self, register_name):
        """
        Returns the value of an address register.
        """

        if register_name not in self._addresses:
            raise RegisterFileException('Unable to find address named {}.'.format(register_name))
        
        self._check_input_lookup(register_name)

        return self._addresses[register_name]
    

    def get_input_lookup(self, register_name):
        """
        Returns the input lookup information for a given register.
        """

        if register_name in self._address_input_lookup:
            return self._address_input_lookup[register_name]

        return super().get_input_lookup(register_name)


    def set_address_input_lookup(self, register_name, input_lookup):
        """
        Sets the input lookup information for a given address register.
        """

        if len(input_lookup) > 0:
            self._address_input_lookup[register_name] = input_lookup


    def restore(self, dump):
        """
        Restores a dump of the register file.
        """

        super().restore(dump)

        self._addresses = copy.deepcopy(dump._addresses)

    def on_function_call(self):
        """
        Callback for function call.
        Each function has its own virtual registers, which all starts from %0.
        The only virtual registers that remains after register allocation
        are the one "removed" then by data layout, which represents only the addresses
        of elements inside the stack. So I must save them before execution of a function
        and restore them after its return.
        """

        self._reg_stack.append(self._addresses)
        self._addresses = {}

        self._reg_stack.append(self._address_input_lookup)
        self._address_input_lookup = {}

        # set first basic block as latest
        self._reg_stack.append(self.last_basic_block)
        self.last_basic_block = '%0'

    def on_function_return(self):
        """
        Callback for function return.
        """

        self.last_basic_block = self._reg_stack.pop()
        self._address_input_lookup = self._reg_stack.pop()
        self._addresses = self._reg_stack.pop()


    def restore(self, dump):
        """
        Restores a dump of the register file.
        """

        super().restore(dump)
        self._addresses = copy.deepcopy(dump._addresses)
        self._address_input_lookup = copy.deepcopy(dump._address_input_lookup)


    def reset(self, main):
        """
        Performs the reset of the register_file (after a cpu reset).
        """

        reg_len = len(self._registers)

        self._addresses = {}
        self._address_input_lookup = {}
        super().reset(main)

        for i in range(0, reg_len):
            register_name = '{}{}'.format(self.reg_prefix, i)
            self._create_register(register_name)


    def diff(self, dump):
        """
        Returns the difference between the current state of the register file and the one saved inside a dump.
        """

        diff = super().diff(dump)

        if self._addresses != dump._addresses:
            reg_keys = list(self._addresses.keys())
            dump_keys = list(dump._addresses.keys())

            common_elements = [item for item in reg_keys if item in dump_keys]
            only_reg_keys = [item for item in reg_keys if item not in dump_keys]
            only_dump_keys = [item for item in dump_keys if item not in reg_keys]

            for i in common_elements:
                if self._addresses[i] != dump._addresses[i]:
                    diff.append({'address_register': i, 'dump_value': copy.deepcopy(dump._addresses[i]), 'current_value': copy.deepcopy(self._addresses[i])})

            for i in only_reg_keys:
                diff.append({'address_register': i, 'dump_value': None, 'current_value': copy.deepcopy(self._addresses[i])})

            for i in only_dump_keys:
                diff.append({'address_register': i, 'dump_value': copy.deepcopy(dump._addresses[i]), 'current_value': None})

        return diff
