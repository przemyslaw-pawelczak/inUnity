import copy
import logging

from ScEpTIC.AST.elements.instruction import Instruction
from ScEpTIC.AST.elements.instructions.other_operations import CallOperation
from ScEpTIC.emulator.io.input import InputManager
from ScEpTIC.exceptions import RuntimeException

class RunInfo:

    def __init__(self, io_type, pc, global_clock, run_id, function_name, io_name, io_value):
        self.io_type = io_type
        self.run_id = run_id
        self.pc = copy.deepcopy(pc)
        self.function_name = function_name
        self.io_name = io_name
        self.io_value = copy.deepcopy(io_value)
        self.global_clock = global_clock
    

    def __str__(self):
        if self.io_type == 'VAR':
            retval = '[{}]\nName: {}\nValue: {}\n'.format(self.io_type, self.io_name, self.io_value)

        elif self.io_type == 'LOG':
            retval = '[{}]\nName: {}\n'.format(self.io_type, self.io_name)
        
        else:
            retval = '[{}]\nName: {}\nFunction name: {}\nValue: {}\n'.format(self.io_type, self.io_name, self.function_name, self.io_value)

        retval += 'Execution clock: {}\nRun id: {}\nInstruction program counter:\n{}'.format(self.global_clock, self.run_id, self.pc.resolve())
        
        return retval


class ProfilingReset(Instruction):
    """
    Reset operation for profiling purposes. Used as marker by the corresponding interruption manager.
    """

    name = 'sceptic_reset'

    def __init__(self, mode, value):
        self._omit_target = True
        self.target = None
        self.mode = mode
        self.value = value
        self.done = False
        super().__init__()


    def _get_mode(self):
        # get address of name var
        address = self.mode.get_val()
        gst = self._vmstate.memory.gst._get_gst_from_address(address)
        return gst.read_string_from_address(address)


    def __str__(self):
        retstr = super().__str__()
        retstr += 'ProfilingReset({})'.format(self.mode)
        return retstr


    def get_val(self):
        return None


    def get_uses(self):
        first_reg = self.mode.get_uses()
        if self.value is None or 'get_uses' not in dir(self.value):
            return first_reg
        
        second_reg = self.value.get_uses()
        return first_reg + second_reg


    def replace_reg_name(self, old_reg_name, new_reg_name):
        self.name.replace_reg_name(old_reg_name, new_reg_name)

        if self.value is None or 'replace_reg_name' not in dir(self.value):
            return

        self.value.replace_reg_name(old_reg_name, new_reg_name)


    def evaluate_reset_condition(self, power_failures):
        mode = self._get_mode()

        if mode == 'once':
            if not self.done:
                self.done = True
                return True

            return False

        elif mode == 'clock':
            target_clock = self.value.get_val()
            return power_failures == target_clock

        elif mode == 'conditional':
            if not self.done:
                condition = self.value.get_val()

                if condition == 1:
                    self.done = True

                return condition == 1

            return False

        if self.tick_count == 0:
            self.tick_count += 1
            return True

        return False


class ProfilingLog(Instruction):
    """
    Profiling log operation for profiling purposes. Used as marker by the corresponding interruption manager.
    """

    tick_count = 0
    name = 'sceptic_log'

    tracking = None
    power_failures = None

    def __init__(self, name, variable):
        self._omit_target = True
        self.target = None
        self.name = name
        self.variable = variable
        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'ProfilingLog({}, {})'.format(self.name, self.variable)
        return retstr


    def get_val(self):
        run_info = self.get_run_info(self.power_failures)
        self.tracking[self.power_failures].append(run_info)

        return None


    def get_run_info(self, run_id):
        # get address of name var
        address = self.name.get_val()
        gst = self._vmstate.memory.gst._get_gst_from_address(address)
        name = gst.read_string_from_address(address)
        
        pc = copy.deepcopy(self._vmstate.register_file.pc)
        global_clock = self._vmstate.global_clock

        if self.variable is None:
            return RunInfo('LOG', pc, global_clock, run_id, '', name, '')

        else:
            value = self.variable.get_val()
            return RunInfo('VAR', pc, global_clock, run_id, '', name, value)


    def get_uses(self):
        first_reg = self.name.get_uses()
        if self.variable is None or 'get_uses' not in dir(self.variable):
            return first_reg

        second_reg = self.variable.get_uses()
        return first_reg + second_reg


    def replace_reg_name(self, old_reg_name, new_reg_name):
        self.name.replace_reg_name(old_reg_name, new_reg_name)
        
        if self.variable is None or 'get_uses' not in dir(self.variable):
            return
        
        self.variable.replace_reg_name(old_reg_name, new_reg_name)


class ProfilingChangeInputVal(Instruction):
    """
    Changes input value at runtime. Used as marker by the corresponding interruption manager.
    """

    tick_count = 0
    name = 'sceptic_change_input'

    def __init__(self, name, value):
        self._omit_target = True
        self.target = None
        self.name = name
        self.value = value
        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'ProfilingChangeInputVal({}, {})'.format(self.name, self.value)
        return retstr


    def get_val(self):
        # get address of name var
        address = self.name.get_val()
        gst = self._vmstate.memory.gst._get_gst_from_address(address)
        name = gst.read_string_from_address(address)

        value = self.value.get_val()

        InputManager.set_input_value(name, value)

        return None


    def get_uses(self):
        first_reg = self.name.get_uses()
        if self.value is None or 'get_uses' not in dir(self.value):
            return first_reg

        second_reg = self.value.get_uses()
        return first_reg + second_reg


    def replace_reg_name(self, old_reg_name, new_reg_name):
        self.name.replace_reg_name(old_reg_name, new_reg_name)
        
        if self.value is None or 'get_uses' not in dir(self.value):
            return
        
        self.value.replace_reg_name(old_reg_name, new_reg_name)



def pre_parse_profiling_log(text, ir_function_prefix):
    """
    Pre parse profiling log, so to avoid errors due to the lack of profiling_log definition in the C source code.
    """

    if ProfilingLog.name in text:
        f_name = ProfilingLog.name

    elif ProfilingReset.name in text:
        f_name = ProfilingReset.name

    elif ProfilingChangeInputVal.name in text:
        f_name = ProfilingChangeInputVal.name

    else:
        return text

    # if ProfilingLog or ProfilingReset
    index = text.index(f_name)

    if text[index-1] == ir_function_prefix:
        name_index = text.index('@', index) + 1
        name = text[name_index]

        if '%' in text[name_index:]:
            var_index = text.index('%', name_index) + 1
            var = text[var_index]

            return ['call', 'void', ir_function_prefix, f_name, '(', 'i8', '*', ir_function_prefix, name, ',', 'i32', '%', var, ')']

        # search for an immediate as second parameter -> ), i32 N)
        next_arg_search = text[name_index:]
        if ')' in next_arg_search:
            first_par = text[name_index:].index(')')

            # -> , i32 N
            if next_arg_search[first_par+1] == ',' and next_arg_search[first_par+2] == 'i32':
                var = next_arg_search[first_par+3]
                return ['call', 'void', ir_function_prefix, f_name, '(', 'i8', '*', ir_function_prefix, name, ',', 'i32', var, ')']

        return ['call', 'void', ir_function_prefix, f_name, '(', 'i8', '*', ir_function_prefix, name, ')']


def process_profiling_calls(ir_function_prefix, functions, declarations):
    """
    Processes the calls to profiling operations in each function.
    """

    # adjust function names with prefix
    ProfilingReset.name = '{}{}'.format(ir_function_prefix, ProfilingReset.name)
    ProfilingLog.name = '{}{}'.format(ir_function_prefix, ProfilingLog.name)
    ProfilingChangeInputVal.name = '{}{}'.format(ir_function_prefix, ProfilingChangeInputVal.name)

    profiling_f_names = [ProfilingReset.name, ProfilingLog.name, ProfilingChangeInputVal.name]

    for f_name in profiling_f_names:
        if f_name in declarations:
            del declarations[f_name]

    # for each function scan the body and
    for function_name in functions:
        function = functions[function_name]

        i = 0

        # scan and alter the code in function body.
        while i < len(function.body):
            line = function.body[i]
            
            # replace in function body the calls to profiling function with the corresponding operation.
            if isinstance(line, CallOperation) and line.name in profiling_f_names:
                function.body[i] = _create_profiling_call(line)

            i += 1

        # update function labels
        function.update_labels()

        # remove from internal calls the profiling functions, so to not consider them during registers allocation
        for f_name in profiling_f_names:
            function._remove_from_calls(f_name)


def _create_profiling_call(line):
    """
    Given a function call to a Profiling function, returns the corresponding operation.
    """

    # check the length of the arguments passed to the function call.

    args_number = len(line.function_args)

    exception_message = 'Wrong parameter count for {} function. They must be a string and a variable pointer!'.format(line.name)

    if line.name == ProfilingLog.name:
        if args_number == 0 or args_number > 2:
            raise RuntimeException(exception_message)
        
        profiling_function = ProfilingLog(line.function_args[0], line.function_args[1] if args_number == 2 else None)

    elif line.name == ProfilingReset.name:
        if args_number == 0 or args_number > 2:
            raise RuntimeException(exception_message)
        
        profiling_function = ProfilingReset(line.function_args[0], line.function_args[1] if args_number == 2 else None)

    elif line.name == ProfilingChangeInputVal.name:
        if args_number != 2:
            raise RuntimeException(exception_message)

        profiling_function = ProfilingChangeInputVal(line.function_args[0], line.function_args[1])

    # copy class parameters
    profiling_function.basic_block_id = line.basic_block_id
    profiling_function.label = line.label
    profiling_function.preds = line.preds
    profiling_function.metadata = line.metadata

    # return the created object
    return profiling_function
