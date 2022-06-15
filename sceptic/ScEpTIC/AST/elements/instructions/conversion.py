import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.instruction import Instruction
from ScEpTIC.exceptions import NotImplementedException, RuntimeException


class ConversionOperation(Instruction):
    """
    AST nodes for the LLVM Bitwise Instructions group
    https://llvm.org/docs/LangRef.html#bitwiseops
    """

    def __init__(self, conversion_type, operand, target_type, target):
        self.conversion_type = conversion_type
        self.operand = operand
        self.target_type = target_type
        self.target = target

        # instructions that do not correspond to any ISA instruction
        if self.conversion_type in ['bitcast', 'addrspacecast', 'inttoptr', 'ptrtoint']:
            self.tick_count = 0

        super().__init__()

    def __str__(self):
        retstr = super().__str__()
        retstr += '{} {} to {}'.format(self.conversion_type, self.operand, self.target_type)
        return retstr


    def get_input_lookup(self):
        """
        Returns the input lookup data for the current operation
        """

        operand = self.operand.get_input_lookup()
        
        return tools.merge_input_lookup_data(operand, tools.build_input_lookup_data(None, None))


    def get_val(self):
        """
        Returns the value obtained from the operation.
        It converts address operands (if present) to relative spaces, applies the operation and converts them back to the absolute space.
        """

        operand = self.operand.get_val()
        
        prefix = None

        # if operand is an address, get prefix and relative address (which can be used in conversion)
        if self._vmstate.memory._is_absolute_address(operand):
            prefix, operand = self._vmstate.memory._parse_absolute_address(operand)

        value = self._get_val(operand)

        # if prefix is set, value is an address. If so, convert it from relative to absolute space.
        if prefix is not None:
            value = self._vmstate.memory._convert_to_absolute_address(prefix, value)

        logging.info('[{}] Executing {} on {} with result {}'.format(self.instruction_type, self.conversion_type, operand, value))

        return value


    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """
        
        return self.operand.get_uses()
    

    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        self.operand.replace_reg_name(old_reg_name, new_reg_name)

        if self.target is not None:
            self.target.replace_reg_name(old_reg_name, new_reg_name)


    def _get_val(self, value):
        """
        Returns the value returned from the operation, given its operands.
        """

        if self.conversion_type == 'addrspacecast':
            # is like bitcast, but for converting the address space
            return value

        elif self.conversion_type == 'fpext':
            value = float(value)
            
            # converts a fp value to a larger-sized one.
            # for how data is represented in the simulator, it does nothing
            return value

        elif self.conversion_type == 'fptosi':
            # fp to signed int conversion
            value = float(value)
            
            dim = len(self.target_type)
            
            # convert to int value
            value = int(round(value))

            # apply max dimension
            value = self.operand.convert_sint_to_sint(value, dim)

            return value

        elif self.conversion_type == 'fptoui':
            # float to unsigned int conversion
            value = float(value)
            
            dim = len(self.target_type)
            
            # convert to int value
            value = int(round(value))

            # apply max dimension
            value = self.operand.convert_sint_to_uint(value, dim)

            # NB: elements in registers / memory are saved as SIGNED int.
            # Operations that uses UNSIGNED operands, first converts the SIGNED operand to UNSIGNED one.
            # (SIGNED VS UNSIGNED is just a mode of interpretation)

            return value

        elif self.conversion_type == 'fptrunc':
            # converts a fp value to a smaller-sized one.
            # for how data is represented in the simulator, it does nothing
            value = float(value)
            
            return value

        elif self.conversion_type == 'bitcast':
            # bitcast does not apply any conversion.
            # it just tells the compiler to treat data as it was already written as "target_type"
            return value

        elif self.conversion_type == 'inttoptr':
            # returns back the integer as memory location (address)
            # for how addresses are represented, it does nothing.
            
            return value

        elif self.conversion_type == 'ptrtoint':
            # returns the memory address as an integer
            # for how addresses are represented, it does nothing.

            return value

        elif self.conversion_type == 'sext':
            value = int(value)
            
            initial_dim = len(self.operand)
            value = self.operand.convert_sint_to_bin(value, initial_dim)

            target_dim = len(self.target_type)
            prefix = value[0] * (target_dim - initial_dim)

            value = prefix + value
            
            return self.operand.convert_bin_to_sint(value)
        
        elif self.conversion_type == 'sitofp':
            # convert an integer to a float
            return float(value)

        elif self.conversion_type == 'uitofp':
            # convert an unsigned integer to a float

            # convert memory cell value to unsigned int.
            value = int(value)
            
            value = self.operand.convert_sint_to_uint(value, len(self.operand))
            
            return float(value)

        elif self.conversion_type == 'trunc':
            dim = len(self.operand)
            value = self.operand.convert_sint_to_bin(int(value), dim)
            
            trunc = dim-len(self.target_type)

            value = self.operand.convert_bin_to_sint(value[trunc:])

            return value

        elif self.conversion_type == 'zext':
            initial_dim = len(self.operand)

            value = self.operand.convert_sint_to_bin(value, initial_dim)

            dim = len(self.target_type)

            value = '0' * (dim - initial_dim) + value

            # for how data is represented, zero expansion does nothing
            return self.operand.convert_bin_to_sint(value)

        # if gets there, the conversion mode is not supported.
        raise NotImplementedException('{} is not supported for now!'.format(self.operation_type))
