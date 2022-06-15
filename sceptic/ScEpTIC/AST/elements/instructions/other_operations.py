import copy
import logging
import math

from ScEpTIC import tools
from ScEpTIC.AST.elements.instruction import Instruction
from ScEpTIC.AST.elements.types import BaseType
from ScEpTIC.exceptions import RuntimeException, RegAllocException, NotImplementedException


class CompareOperation(Instruction):
    """
    AST node of the LLVM Other Instructions group - Compare Instruction
    https://llvm.org/docs/LangRef.html#otherops
    """

    def __init__(self, target, first_operand, second_operand, condition, comparation_type, operation_code):
        self.target = target
        self.first_operand = first_operand
        self.second_operand = second_operand
        self.condition = condition
        self.type = comparation_type
        self.operation_code = operation_code

        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'cmp {}: {} vs {}'.format(self.condition, self.first_operand, self.second_operand)
        return retstr


    @staticmethod
    def is_qnan(value):
        """
        Returns if a value is a QNAN
        """

        # if value is None -> QNAN (for my memory representation)
        return value is None or math.isnan(value)


    @staticmethod
    def is_one_qnan(value1, value2):
        """
        Returns if at least one of two values are QNAN
        """

        return CompareOperation.is_qnan(value1) or CompareOperation.is_qnan(value2)


    def _check_prefix(self, prefix1, prefix2):
        """
        Verify if address prefixes are consistent.
        """

        if prefix1 != prefix2:
            raise RuntimeException('Unable to compare different address spaces ({} with {}) for the compare operation {}.'.format(prefix1, prefix2, self.condition))


    def get_val(self):
        """
        Returns the value obtained from the operation.
        It converts address operands (if present) to relative spaces, and applies the comparisons.
        """

        dim = len(self.first_operand.type)
        first_operand = self.first_operand.get_val()
        second_operand = self.second_operand.get_val()

        # address prefixes (populated if an operand is an address)
        prefix1 = None
        prefix2 = None

        # if first_operand is an address, get prefix and relative address (which can be used in comparisons)
        if self._vmstate.memory._is_absolute_address(first_operand):
            prefix1, first_operand = self._vmstate.memory._parse_absolute_address(first_operand)

        # if second_operand is an address, get prefix and relative address (which can be used in comparisons)
        if self._vmstate.memory._is_absolute_address(second_operand):
            prefix2, second_operand = self._vmstate.memory._parse_absolute_address(second_operand)

        # adjust prefixes if only one element is an address
        # NB: is possible to compare an address with a direct value, and in this case the prefix can be ignored.
        # (so I just copy it to the other prefix)
        if prefix1 is None:
            prefix1 = prefix2

        elif prefix2 is None:
            prefix2 = prefix1
        
        logging.info('[{}] Executing {} {}{}, {}{}'.format(self.instruction_type, self.condition, '' if prefix1 is None else prefix1, first_operand, '' if prefix2 is None else prefix2, second_operand))

        # comparison types
        if self.condition == 'eq':
            return prefix1 == prefix2 and first_operand == second_operand

        elif self.condition == 'ne':
            return prefix1 != prefix2 or first_operand != second_operand

        elif self.condition == 'sgt':
            self._check_prefix(prefix1, prefix2)
            return first_operand > second_operand

        elif self.condition == 'sge':
            self._check_prefix(prefix1, prefix2)
            return first_operand >= second_operand

        elif self.condition == 'slt':
            self._check_prefix(prefix1, prefix2)
            return first_operand < second_operand

        elif self.condition == 'sle':
            self._check_prefix(prefix1, prefix2)
            return first_operand <= second_operand

        elif self.condition == 'ugt':
            self._check_prefix(prefix1, prefix2)
            
            if self.operation_code == 'fcmp':
                # unordered check -> true if one is QNAN
                return self.is_one_qnan(first_operand, second_operand) or first_operand > second_operand

            else:
                # converts to unsigned ints
                first_operand = self.first_operand.convert_sint_to_uint(first_operand, dim)
                second_operand = self.second_operand.convert_sint_to_uint(second_operand, dim)
                
                return first_operand > second_operand

        elif self.condition == 'uge':
            self._check_prefix(prefix1, prefix2)

            if self.operation_code == 'fcmp':
                # unordered check -> true if one is QNAN
                return self.is_one_qnan(first_operand, second_operand) or first_operand >= second_operand

            else:
                # converts to unsigned ints
                first_operand = self.first_operand.convert_sint_to_uint(first_operand, dim)
                second_operand = self.second_operand.convert_sint_to_uint(second_operand, dim)
                
                return first_operand >= second_operand

        elif self.condition == 'ult':
            self._check_prefix(prefix1, prefix2)

            if self.operation_code == 'fcmp':
                # unordered check -> true if one is QNAN
                return self.is_one_qnan(first_operand, second_operand) or first_operand < second_operand

            else:
                # converts to unsigned ints
                first_operand = self.first_operand.convert_sint_to_uint(first_operand, dim)
                second_operand = self.second_operand.convert_sint_to_uint(second_operand, dim)
            
                return first_operand < second_operand

        elif self.condition == 'ule':
            self._check_prefix(prefix1, prefix2)

            if self.operation_code == 'fcmp':
                # unordered check -> true if one is QNAN
                return self.is_one_qnan(first_operand, second_operand) or first_operand <= second_operand
                
            else:
                # converts to unsigned ints
                first_operand = self.first_operand.convert_sint_to_uint(first_operand, dim)
                second_operand = self.second_operand.convert_sint_to_uint(second_operand, dim)
                
                return first_operand <= second_operand
        
        elif self.condition == 'true':
            return True

        elif self.condition == 'false':
            return False

        elif self.condition == 'ord':
            self._check_prefix(prefix1, prefix2)
            return not self.is_one_qnan(first_operand, second_operand)
        
        elif self.condition == 'oeq':
            return not self.is_one_qnan(first_operand, second_operand) and prefix1 == prefix2 and first_operand == second_operand
        
        elif self.condition == 'one':
            return not self.is_one_qnan(first_operand, second_operand) and (prefix1 != prefix2 or first_operand != second_operand)
        
        elif self.condition == 'ogt':
            self._check_prefix(prefix1, prefix2)
            return not self.is_one_qnan(first_operand, second_operand) and first_operand > second_operand

        elif self.condition == 'oge':
            self._check_prefix(prefix1, prefix2)
            return not self.is_one_qnan(first_operand, second_operand) and first_operand >= second_operand
        
        elif self.condition == 'olt':
            self._check_prefix(prefix1, prefix2)
            return not self.is_one_qnan(first_operand, second_operand) and first_operand < second_operand

        elif self.condition == 'ole':
            self._check_prefix(prefix1, prefix2)
            return not self.is_one_qnan(first_operand, second_operand) and first_operand <= second_operand
        
        elif self.condition == 'uno':
            self._check_prefix(prefix1, prefix2)
            return self.is_one_qnan(first_operand, second_operand)
        
        elif self.condition == 'ueq':
            return self.is_one_qnan(first_operand, second_operand) or (prefix1 == prefix2 and first_operand == second_operand)
        
        elif self.condition == 'une':
            return self.is_one_qnan(first_operand, second_operand) or (prefix1 != prefix2 or first_operand != second_operand)

        # if gets there, the comparison mode is not supported.
        raise NotImplementedException('Comparison mode "{}" not supported for now!'.format(self.condition))

    
    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        first_reg = self.first_operand.get_uses()
        second_reg = self.second_operand.get_uses()
        return first_reg + second_reg


    def get_input_lookup(self):
        """
        Returns the input lookup data for the current operation
        """

        first = self.first_operand.get_input_lookup()
        second = self.second_operand.get_input_lookup()

        return tools.merge_input_lookup_data(first, second)


    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        self.first_operand.replace_reg_name(old_reg_name, new_reg_name)
        self.second_operand.replace_reg_name(old_reg_name, new_reg_name)
        self.target.replace_reg_name(old_reg_name, new_reg_name)


class PhiOperation(Instruction):
    """
    AST node of the LLVM Other Instructions group - Phi Instruction
    https://llvm.org/docs/LangRef.html#otherops
    """

    def __init__(self, target, return_type, values):
        self.target = target
        self.type = return_type
        # values is a dict with label as keys {labelid: value}
        self.values = values

        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'phi {}: {}'.format(self.type, self.values)
        return retstr


    def get_val(self):
        """
        Returns the value obtained from the operation.
        """

        # get the basic block from which the current one is entered.
        label = self._vmstate.register_file.last_basic_block

        if label not in self.values:
            raise RuntimeException('Basic Block {} not present in the choices of phi operation.'.format(label))

        # get value
        value = self.values[label].get_val()

        logging.info('[{}] Executing PHI operation with result {} ({} taken).'.format(self.instruction_type, value, label))
        
        return value

    
    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        uses = []
        for value in self.values:
            value = self.values[value].get_uses()
            uses = uses + value

        return uses

    
    def get_input_lookup(self):
        """
        Returns the input lookup data for the current operation
        """

        label = self._vmstate.register_file.last_basic_block
        
        return self.values[label].get_input_lookup()


    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        for value in self.values:
            self.values[value].replace_reg_name(old_reg_name, new_reg_name)

        self.target.replace_reg_name(old_reg_name, new_reg_name)


class SelectOperation(Instruction):
    """
    AST node of the LLVM Other Instructions group - Select Instruction
    https://llvm.org/docs/LangRef.html#otherops
    """

    def __init__(self, target, condition, first_operand, second_operand):
        self.target = target
        self.condition = condition
        self.first_operand = first_operand
        self.second_operand = second_operand

        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'select {}: {}, {}'.format(self.condition, self.first_operand, self.second_operand)
        return retstr


    def get_val(self):
        """
        Returns the result of the operation.
        """

        # if condition resolves to 1 returns the first operand, otherwise the second one.
        condition = self.condition.get_val()

        logging.info('[{}] Executing Select operation with condition {}.'.format(self.instruction_type, condition))
        
        if int(condition) == 1:
            return self.first_operand.get_val()

        else:
            return self.second_operand.get_val()


    def get_input_lookup(self):
        """
        Returns the input lookup data for the current operation
        """

        condition = self.condition.get_val()

        if int(condition) == 1:
            return self.first_operand.get_input_lookup()

        else:
            return self.second_operand.get_input_lookup()


    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        first_reg = self.first_operand.get_uses()
        second_reg = self.second_operand.get_uses()
        cond_reg = self.condition.get_uses()

        return first_reg + second_reg + cond_reg


    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        self.first_operand.replace_reg_name(old_reg_name, new_reg_name)
        self.second_operand.replace_reg_name(old_reg_name, new_reg_name)
        self.condition.replace_reg_name(old_reg_name, new_reg_name)
        self.target.replace_reg_name(old_reg_name, new_reg_name)


class CallOperation(Instruction):
    """
    AST node of the LLVM Other Instructions group - Call Instruction
    https://llvm.org/docs/LangRef.html#otherops
    """

    # push pc
    # push ebp
    # esp <- ebp
    # pc = 0x...
    # args are pushed/loaded by previously-inserted operations
    tick_count = 4

    ignore = []

    def __init__(self, target, function_name, return_type, function_signature, function_args, attrs):
        self.target = target
        self.name = function_name
        self.type = return_type
        # is a possible empty list containing the function signature when var_args is used
        # is a list of Type with additional attributes field
        self.function_signature = function_signature
        # is a list of Values with additional attributes field.
        self.function_args = function_args

        # all attributes used for back-end / middle-end optimizations.
        # the only one needed are from 'return' and are zeroext and signext.
        # the same applies for the function arguments's attributes.
        # for how data is represented, only signext applies a modification on data,
        # and since functions are user-defined and no 1bit data structure exists in C,
        # sext won't have any unattended behaviour (e.g. i1 1 = -1), so can be omitted.
        self.attributes = attrs

        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'call {}({})'.format(self.name, self.function_args)
        return retstr


    def get_function_max_reg_usage(self):
        """
        Returns the number of physical registers used by this function.
        """

        function = self._vmstate.functions[self.name]

        if 'max_reg_usage' not in function.__dict__:
            raise RegAllocException('Register allocation not done on function {}'.format(self.name))
        
        return function.max_reg_usage


    def run(self):
        """
        Runs the call operation.
        """

        logging.info('[{}] Calling function {}.'.format(self.instruction_type, self.name))

        # instructions to be skipped (checkpoint, restore)
        if self.name in self.ignore:
            self._vmstate.register_file.pc.increment_pc()
            return
        
        args = []
        input_lookups = []

        # In a real scenario, args are saved onto the stack. In this case, instead, they are re-loaded before the
        # function call and directly passed as values.
        # The loading of each arguments results in a very similar number of operations as saving them into the stack
        # but since the RegisterFile is stacked when the function call happens, I need to save their values and restore
        # them back as virtual_registers or address_registers (in case of physical regfile) to be able to use them.
        for arg in self.function_args:
            arg_val = arg.get_val()
            args.append(arg_val)

            if self._vmstate.input_lookup_enabled:
                if arg.value_class == 'virtual_reg':
                    input_lookup_data = self._vmstate.register_file.get_input_lookup(arg.value)
                    input_lookups.append(input_lookup_data)
                else:
                    input_lookups.append(None)

        # emulate stacking of arguments for stack's anomalies analysis
        arg_count = len(self.function_args)
        saved_params_number = min(arg_count - self._vmstate.register_file.param_regs_count, 0)

        arg_count -= 1

        # push parameters in reverse order. NB: some parameters are passed using registers
        for i in range(arg_count, arg_count-saved_params_number, -1):
            arg = self.function_args[i]
            arg_len = len(arg.type)
            arg_val = arg.get_val()

            if self._vmstate.do_data_anomaly_check:
                self._vmstate.function_call_lookup['args'].append(self._vmstate.memory.stack.top_address)
            
            self._vmstate.memory.stack.push(arg_len, arg_val, 'function argument')
        
        # callback
        self._vmstate.on_function_call(self.name)
        self._vmstate.global_clock += self.tick_count

        f_args = self._vmstate.functions[self.name].arguments
        var_arg = BaseType('var_args', '8')

        for i in range(0, len(f_args)):
            is_var_arg = f_args[i].base_type == var_arg
            
            # if is a variable argument, from now insert elements inside a single list
            if is_var_arg:
                arg = []
                for j in range(i, len(args)):
                    arg.append(args[j])
            else:
                arg = args[i]

            # NB: here I use write_address, since for virtual regfile is like write()
            # and for physical one is needed since the stack placement is emulated as a sequence of
            # laod before their actual usage.
            target = '%{}'.format(i)
            self._vmstate.register_file.write_address(target, arg)
            
            # set input lookup
            if self._vmstate.input_lookup_enabled and not is_var_arg and input_lookups[i] is not None:
                self._vmstate.register_file.set_address_input_lookup(target, input_lookups[i])

            # if is var_arg, all arguments have been passed, so stop
            if is_var_arg:
                break


    def get_type_from_virtual_reg(self, virtual_reg):
        """
        Returns the type of an argument given its virtual register name.
        """

        for arg in self.function_args:
            # if the virtual reg is in the uses of the argument, the
            # given type is the one of the argument.
            if virtual_reg in arg.get_uses():
                
                # returns a copy so to not change the original element
                return copy.deepcopy(arg.type)

        return None


    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        uses = []
        for arg in self.function_args:
            uses = uses + arg.get_uses()

        return uses

    
    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        for arg in self.function_args:
            arg.replace_reg_name(old_reg_name, new_reg_name)

        if self.target is not None:
            self.target.replace_reg_name(old_reg_name, new_reg_name)


class VaArgOperation(Instruction):
    """
    AST node of the LLVM Other Instructions group - VaArg Instruction
    NOT SUPPORTED IN ScEpTIC
    https://llvm.org/docs/LangRef.html#otherops
    """

    def __init__(self, target, element, arg_type):
        self.target = target
        self.element = element
        self.type = arg_type

        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'va_arg {} {}'.format(self.condition, self.element, self.type)
        return retstr


    def run(self):
        raise RuntimeException('va_arg llvm instruction not supported for now.')
