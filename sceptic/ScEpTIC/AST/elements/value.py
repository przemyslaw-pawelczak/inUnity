import logging
import struct

from ScEpTIC import tools
from ScEpTIC.exceptions import MemoryException, NotImplementedException

class Value:
    """
    AST node for data representation (immediate, register data, etc)
    """

    _vmstate = None

    def __init__(self, value_class, operand_value, value_type):
        self.value_class = value_class
        self.value = operand_value
        self.type = value_type


    def __repr__(self):
        return 'Value({}, {}, {})'.format(self.value_class, self.value, self.type)


    def __str__(self):
        if self.type is None:
            return str(self.value)

        return 'Value: ({}) {}'.format(self.type, self.value)


    def __len__(self):
        return len(self.type)


    def get_val(self):
        """
        Retrieve and returns the value represented by the object.
        """

        if self._vmstate is None:
            raise MemoryException('VM Status not initialized!')

        if self.value_class == 'immediate':
            value = self._resolve_immediate()

        elif self.value_class == 'array_val':
            value = self._resolve_array_val()

        elif self.value_class == 'virtual_reg':
            value = self._vmstate.register_file.read(self.value)

        elif self.value_class == 'global_var':
            value = self._vmstate.memory.gst.get_symbol_address(self.value)

        elif self.value_class == 'vector':
            raise NotImplementedException('Vector operations not supported at the moment. Please compile with a different target.')
        
        elif self.value_class == 'address':
            # GetElementPointerOperation has method get_val that resolves the correct value
            value = self.value.get_val()

        elif self.value_class == 'conversion':
            # ConversionOperation has method get_val that resolves the correct value
            value = self.value.get_val()

        elif self.value_class == 'metadata':
            # appears only in @llvm.dbg functions, so no need to resolve that address
            raise ValueError('Metadata should not be present in running functions.')

        logging.info('[Value] Resolved value of {} with {}.'.format(self.value, value))

        return value


    def get_input_lookup(self):
        """
        Returns the input lookup information for the current Value object.
        """

        if self._vmstate.input_lookup_enabled:
            if self.value_class == 'virtual_reg':
                return self._vmstate.register_file.get_input_lookup(self.value)

            elif self.value_class == 'address':
                return self.value.get_input_lookup()

            elif self.value_class == 'conversion':
                return self.value.get_input_lookup()

        return tools.build_input_lookup_data(None, None)


    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this value.
        (used by register allocation)
        """

        if self.value_class == 'virtual_reg':
            return [self.value]

        elif self.value_class == 'address':
            return self.value.get_uses()

        elif self.value_class == 'conversion':
            return self.value.get_uses()

        return []


    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register contained in this Value object.
        (used by register allocation)
        """

        if self.value_class == 'virtual_reg':
            if self.value == old_reg_name:
                self.value = new_reg_name

        elif self.value_class == 'address':
            self.value.replace_reg_name(old_reg_name, new_reg_name)

        elif self.value_class == 'conversion':
            self.value.replace_reg_name(old_reg_name, new_reg_name)


    def _resolve_immediate(self):
        """
        Resolves the value of a immediate.
        """

        if self.value is None or self.value == 'null':
            return None

        if self.value == 'true':
            return 1

        if self.value == 'false':
            return 0

        try:
            return int(self.value)
        except ValueError:
            pass

        try:
            return float(self.value)
        except ValueError:
            pass

        if 'e+' in self.value:
            return float(self.value)

        if '0x' in self.value:
            # self.value[2:] to remove 0x
            # each value is converted as a double from llvm, even if is a float

            # NB: target architecture could be in little endian (e in target_datalayout)
            # or big endian (E in target_datalayout). The conversion in the llvm ir stays the same,
            # independently from the type of endianness used by the backend compiler.
            # So the endianness conversion stays ! (network - big-endian)
            return struct.unpack('!d', bytes.fromhex(self.value[2:]))[0]

        if self.value == 'zeroinitializer':
            composition = self.type.get_memory_composition(True)
            
            for i in range(0, len(composition)):
                composition[i] = 0

            return composition

        return self.value


    def _resolve_array_val(self):
        """
        Resolves the value of array initialization.
        """

        flat_values = []
        tools.inf_depth_lst_flat(self.value, flat_values)

        for i in range(0, len(flat_values)):
            flat_values[i] = flat_values[i].get_val()

        return flat_values


    @staticmethod
    def convert_sint_to_bin(val, bits):
        """
        Converts a signed integer to its binary representation, using a certain number of bits
        """

        format_str = '{:0'+str(bits)+'b}'

        if val < 0:
            # all 1s
            mask = int('1' * bits, 2)
            val = format_str.format(val & mask)
        else:
            val = format_str.format(val)

        # return correct bit dimension
        return val[-bits:]

    @staticmethod
    def convert_uint_to_bin(val, bits):
        """
        Converts an unsigned integer to its binary representation.
        For how data is represented, it is the same as converting a signed integer to binary.
        """

        return Value.convert_sint_to_bin(val, bits)


    @staticmethod
    def convert_bin_to_uint(val):
        """
        Converts a number in binary format to its equivalent unsigned decimal.
        """

        return int(val, 2)


    @staticmethod
    def convert_bin_to_sint(val):
        """
        Converts a number in binary format to its equivalent signed decimal.
        """

        if val[0] == '0':
            return int(val, 2)

        return int(val[1:], 2) - (2 ** (len(val) - 1))


    @staticmethod
    def convert_sint_to_uint(val, bits):
        """
        Converts a number in signed integer form to its equivalent unsigned integer.
        """

        val = Value.convert_sint_to_bin(val, bits)
        return Value.convert_bin_to_uint(val)


    @staticmethod
    def convert_uint_to_sint(val, bits):
        """
        Converts a number in unsigned integer form to its equivalent signed integer.
        """

        val = Value.convert_uint_to_bin(val, bits)
        return Value.convert_bin_to_sint(val)


    @staticmethod
    def convert_sint_to_sint(val, bits):
        """
        Convert a signed integer to a signed integer, using a maximum number of bits.
        """

        val = Value.convert_sint_to_bin(val, bits)
        return Value.convert_bin_to_sint(val)
