import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.instruction import Instruction
from ScEpTIC.exceptions import RuntimeException, NotImplementedException

class BinaryOperation(Instruction):
    """
    AST nodes for the LLVM Binary Instructions group
    https://llvm.org/docs/LangRef.html#binaryops

    NB: each result is stored as SIGNED int, even if the operation is unsigned.
    The sign bit is an interpretation of UNSIGNED operations, which will manage that by converting the int to its unsigned equivalent.
    """
    
    def __init__(self, operation_type, first_operand, second_operand, target, is_bitwise, specific_attributes):
        self.operation_type = operation_type
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.target = target
        self.is_bitwise = is_bitwise
        
        # just used to determine if a result is a "poison value", which is for back-end optimizations.
        self.exact = 'exact' in specific_attributes
        self.no_unsigned_wrap = 'nuw' in specific_attributes
        self.no_signed_wrap = 'nsw' in specific_attributes

        super().__init__()

    def __str__(self):
        retstr = super().__str__()
        retstr += '{} {}, {}'.format(self.operation_type, self.first_operand, self.second_operand)
        return retstr


    def get_input_lookup(self):
        """
        Returns the input lookup data for the current operation
        """

        first = self.first_operand.get_input_lookup()
        second = self.second_operand.get_input_lookup()

        return tools.merge_input_lookup_data(first, second)


    def get_val(self):
        """
        Returns the value obtained from the operation.
        It converts address operands (if present) to relative spaces, applies the operation and converts them back to the absolute space.
        """
        
        first_operand = self.first_operand.get_val()
        second_operand = self.second_operand.get_val()
        
        # address prefixes (populated if an operand is an address)
        prefix1 = None
        prefix2 = None

        # if first_operand is an address, get prefix and relative address (which can be used in operations)
        if self._vmstate.memory._is_absolute_address(first_operand):
            prefix1, first_operand = self._vmstate.memory._parse_absolute_address(first_operand)

        # if second_operand is an address, get prefix and relative address (which can be used in operations)
        if self._vmstate.memory._is_absolute_address(second_operand):
            prefix2, second_operand = self._vmstate.memory._parse_absolute_address(second_operand)

        # normalize prefixes: if one is none, just copy from the other.
        if prefix1 is None:
            prefix1 = prefix2

        elif prefix2 is None:
            prefix2 = prefix1

        val = self._get_val(first_operand, second_operand)

        # if prefix is set the result is an address, so I must convert it from relative to absolute space.
        if prefix1 is not None:
            # NB: prefixes must be the same
            if prefix1 != prefix2:
                raise RuntimeException('Uncompatible address space {} {} for binary operation {}.'.format(prefix1, prefix2, self.operation_type))

            val = self._vmstate.memory._convert_to_absolute_address(prefix1, val)

        logging.info('[{}] Executing {} {}, {} with result {}'.format(self.instruction_type, self.operation_type, first_operand, second_operand, val))

        return val


    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        first_reg = self.first_operand.get_uses()
        second_reg = self.second_operand.get_uses()
        return first_reg + second_reg


    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        self.first_operand.replace_reg_name(old_reg_name, new_reg_name)
        self.second_operand.replace_reg_name(old_reg_name, new_reg_name)
        self.target.replace_reg_name(old_reg_name, new_reg_name)


    def _get_val(self, first_operand, second_operand):
        """
        Returns the value returned from the operation, given its operands.
        """

        dim = len(self.first_operand.type)

        if self.operation_type == 'add':
            # force encoding
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            val = first_operand + second_operand
            # force a number of bits
            
            return self.first_operand.convert_sint_to_sint(val, dim)

        elif self.operation_type == 'fadd':
            first_operand = float(first_operand)
            second_operand = float(second_operand)
            
            return first_operand + second_operand

        elif self.operation_type == 'sub':
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            val = first_operand - second_operand
            
            return self.first_operand.convert_sint_to_sint(val, dim)

        elif self.operation_type == 'fsub':
            first_operand = float(first_operand)
            second_operand = float(second_operand)
            
            return first_operand - second_operand

        elif self.operation_type == 'mul':
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            val = int(first_operand * second_operand)
            
            return self.first_operand.convert_sint_to_sint(val, dim)

        elif self.operation_type == 'fmul':
            first_operand = float(first_operand)
            second_operand = float(second_operand)
            
            return float(first_operand * second_operand)

        elif self.operation_type == 'udiv':
            # unsigned operations considers their operands as unsigned.
            # http://lists.llvm.org/pipermail/llvm-dev/2017-July/115975.html
            dim = len(self.first_operand)
            
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            first_operand = self.first_operand.convert_sint_to_uint(first_operand, dim)
            second_operand = self.second_operand.convert_sint_to_uint(second_operand, dim)

            val = int(first_operand // second_operand)

            # result is unsigned. Memory cells in my representation uses signed only.
            return self.first_operand.convert_uint_to_sint(val, dim)

        elif self.operation_type == 'sdiv':
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            val = int(first_operand // second_operand)
            
            return self.first_operand.convert_sint_to_sint(val, dim)

        elif self.operation_type == 'fdiv':
            return float(first_operand / second_operand)

        elif self.operation_type == 'urem':
            # unsigned operations considers their operands as unsigned.
            # http://lists.llvm.org/pipermail/llvm-dev/2017-July/115975.html
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            dim = len(self.first_operand)
            first_operand = self.first_operand.convert_sint_to_uint(first_operand, dim)
            second_operand = self.second_operand.convert_sint_to_uint(second_operand, dim)

            val = int(first_operand % second_operand)

            # result is unsigned. Memory cells in my representation uses signed only.
            return self.first_operand.convert_uint_to_sint(val, dim)

        elif self.operation_type == 'srem':
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            val = int(first_operand % second_operand)
            
            return self.first_operand.convert_sint_to_sint(val, dim)

        elif self.operation_type == 'frem':
            first_operand = float(first_operand)
            second_operand = float(second_operand)
            
            return float(first_operand % second_operand)

        elif self.operation_type == 'shl':
            # logic implemented to overcome discrepancies between signed and unsigned results
            # e.g. -1 << 2 != 65535 << 2 for 16bit operations

            first_operand = self.first_operand.convert_sint_to_bin(first_operand, dim)
            sh_len = int(second_operand)

            shifted = first_operand[sh_len:]+sh_len*'0'
            
            return self.first_operand.convert_bin_to_sint(shifted)

        elif self.operation_type == 'lshr':
            # logical shift right: append 0 to added left bits
            
            first_operand = self.first_operand.convert_sint_to_bin(first_operand, dim)
            sh_len = int(second_operand)

            shifted = sh_len*'0'+first_operand[:dim-sh_len]
            
            return self.first_operand.convert_bin_to_sint(shifted)

        elif self.operation_type == 'ashr':
            # arithmetical shift right: append sign bit to added left bits
            
            first_operand = self.first_operand.convert_sint_to_bin(first_operand, dim)
            sh_len = int(second_operand)

            shifted = sh_len*first_operand[0]+first_operand[:dim-sh_len]
            
            return self.first_operand.convert_bin_to_sint(shifted)

        elif self.operation_type == 'and':
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            return int(first_operand & second_operand)

        elif self.operation_type == 'or':
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            return int(first_operand | second_operand)

        elif self.operation_type == 'xor':
            first_operand = int(first_operand)
            second_operand = int(second_operand)
            
            return int(first_operand ^ second_operand)

        # if gets there, the operation is not supported right now.
        raise NotImplementedException('{} is not supported for now!'.format(self.operation_type))
