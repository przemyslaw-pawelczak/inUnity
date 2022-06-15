import copy
import logging

from ScEpTIC import tools
from ScEpTIC.AST import builtins
from ScEpTIC.AST import register_allocation
from ScEpTIC.AST.builtins.linker import BuiltinLinker
from ScEpTIC.AST.elements.instruction import Instruction
from ScEpTIC.AST.elements.instructions.termination_instructions import ReturnOperation
from ScEpTIC.AST.elements.types import Type
from ScEpTIC.AST.elements.value import Value
from ScEpTIC.emulator.intermittent_executor import profiling
from ScEpTIC.emulator.memory.virtual_memory import VirtualMemory, VirtualMemoryCell
from ScEpTIC.emulator.register_file.program_counter import ProgramCounter
from ScEpTIC.emulator.stats import ScEpTICStats
from ScEpTIC.exceptions import ConfigurationException, InitializationException, MemoryException, RuntimeException, StopAnomalyFoundException, StopException

from . import memory
from . import register_file


class VMState:
    """
    State of the ScEpTIC execution environment
    """

    def __init__(self, program_configuration, register_file_configuration, memory_configuration, execution_depth):
        logging.debug('Initializing VMState.')
        self.validate_program_configuration(program_configuration)
        self.validate_execution_depth(execution_depth)

        self.execution_depth = execution_depth
        self.stop_on_first_anomaly = False
        
        # Used for anomaly checks (data, input); auto-configured by InterruptionManager
        self.do_data_anomaly_check = False
        self.input_lookup_enabled = False
        self.collect_memory_trace = False
        
        # Used for anomaly check using memory traces
        self.memory_trace = {}
        self.memory_trace_prefixes = []

        self.anomalies = []
        self.profiling = {}
        self.observations = {}
        
        # initialize Register File and program counter
        ProgramCounter._vmstate = self
        self.register_file = register_file.create_register_file(register_file_configuration)
        self.register_file._vmstate = self

                
        # initialize Memory
        VirtualMemory._vmstate = self
        VirtualMemoryCell._vmstate = self
        self.memory = memory.Memory(memory_configuration)
        Type.address_dimension = self.memory.address_dimension

        if self.memory.memory_positions['stack'] == 'nvm':
            self.memory_trace_prefixes.append(self.memory.address_prefixes['stack'])

        if self.memory.memory_positions['heap'] == 'nvm':
            self.memory_trace_prefixes.append(self.memory.address_prefixes['heap'])

        if 'nvm' in self.memory.memory_positions['gst']:
            self.memory_trace_prefixes.append(self.memory.address_prefixes['nvm_gst'])
        
        # For dynamic checkpoint needs to be True
        # For static checkpoint needs to be False
        # (Automatically configured by interruption manager)
        self.raise_memory_anomaly_exceptions = True

        # used by interruption manager
        self.trigger_reset_and_restore = False

        # used by regiser allocation for saving registers, so to not interfere with the stack content (and thus with anomalies)
        self.reg_saving_pool = []

        # used to differentiate events
        self.global_clock = 0
        self.checkpoint_clock = 0

        # used to map a checkpoint clock to a program counter
        self.checkpoint_clock_pc_maps = {}

        # will contain the return value of the main function
        self.main_return_value = None

        # Force stop
        self.force_stop = False

        # Link VMState to Value
        Value._vmstate = self
        Instruction._vmstate = self
        
        # set main function name
        self._main_function_name = program_configuration['ir_function_prefix'] + program_configuration['main_function_name']
        self._main_function_len = 0
        self.ir_function_prefix = program_configuration['ir_function_prefix']
        BuiltinLinker.prefix = program_configuration['ir_function_prefix']

        # before/after functions
        self.custom_exec_names = {
            'after_checkpoint'  : program_configuration['ir_function_prefix'] + program_configuration['after_checkpoint_function_name'],
            'after_restore'     : program_configuration['ir_function_prefix'] + program_configuration['after_restore_function_name'],
            'before_checkpoint' : program_configuration['ir_function_prefix'] + program_configuration['before_checkpoint_function_name'],
            'before_restore'    : program_configuration['ir_function_prefix'] + program_configuration['before_restore_function_name'],
        }

        # lookup information for stack anomalies
        self._init_function_call_lookup()

        self.stats = ScEpTICStats()

        logging.info('VMState initialized.')


    def _init_function_call_lookup(self):
        """
        Initializes function call lookup information.
        """

        self.function_call_lookup = {'regs': [], 'args': [], 'pc': None, 'ebp': None}


    def init_gst(self, global_vars):
        """
        Initializes the global symbol table.
        """

        logging.debug('Initializing Global Symbol Table')

        for name in global_vars:
            global_var = global_vars[name]
            section = global_var.section
            composition = global_var.type.get_memory_composition(True)
            initial_val = global_var.initial_val.get_val()
            
            # force a list for initial value, since composition is always a list
            if initial_val is not None and not isinstance(initial_val, list):
                initial_val = [initial_val]
            
            self.memory.gst.allocate(name, section, composition, initial_val)

        self.memory.gst.set_state_as_base_state()


    def init_code(self, functions, declarations):
        """
        Stores the function's code information to be run and performs register allocation if required.
        """

        logging.debug('Initializing Code')
        
        self.functions = functions
        
        if self._main_function_name not in self.functions:
            raise ConfigurationException('Unable to find main function "{}" in the provided code.'.format(self._main_function_name))

        self.register_file.pc.update(self._main_function_name, 0)
        self.checkpoint_clock_pc_maps[0] = copy.deepcopy(self.register_file.pc)

        # load builtins
        builtins.load_libraries()
        builtins.link_builtins()
        
        # process profiling markers
        profiling.process_profiling_calls(self.ir_function_prefix, self.functions, declarations)

        if len(declarations) > 0:
            raise InitializationException('The following functions do not have any definition:\n{}'.format(declarations.keys()))

        if self.register_file.requires_register_allocation:
            # load the correct register allocator
            allocator = register_allocation.get_register_allocator(self.register_file.allocation_module_prefix, self.register_file.allocation_module, self.register_file.allocation_function)
            allocator(self.functions, len(self.register_file), self.register_file.reg_prefix, self.register_file.spill_prefix, self.register_file.spill_type)

        self._main_function_len = len(self.functions[self._main_function_name])

        for name in self.functions:
            self.functions[name].adjust_alloca_ticks()

        actual_calls = {}
        # Adjust return operation for functions executed before/after checkpoint/restore
        for name, f_name in self.custom_exec_names.items():
            if f_name in self.functions:
                actual_calls[name] = {'name': f_name, 'ret_ops': []}

                for instruction in self.functions[f_name].body:
                    if isinstance(instruction, ReturnOperation):
                        instruction.update_pc = False
                        actual_calls[name]['ret_ops'].append(instruction)

        self.custom_exec_names = actual_calls


    def on_function_call(self, function_name):
        """
        Callback that executes the operations needed before executing a function call.
        """

        logging.debug("Called on_function_call({})".format(function_name))

        if function_name not in self.functions:
            raise RuntimeException('Unable to execute function call to "{}": function not found.'.format(function_name))

        # callback for registers
        self.register_file.on_function_call()

        # save program counter
        pc = self.register_file.pc.save()
        
        if self.do_data_anomaly_check:
            self.function_call_lookup['pc'] = self.memory.stack.top_address
        
        self.memory.stack.push(self.memory.address_dimension, pc, 'PC')

        
        # save tracking informations
        self.register_file.pc._pc_tracking.append(pc)
        
        # save stack base pointer
        ebp = self.register_file.ebp
        
        if self.do_data_anomaly_check:
            self.function_call_lookup['ebp'] = self.memory.stack.top_address
        
        self.memory.stack.push(self.memory.address_dimension, ebp, 'EBP')
        
        # update ebp
        self.register_file.ebp = self.memory.stack.top_address

        # update pc with function_name at instruction #0
        self.register_file.pc.update(function_name, 0)


    def on_function_return(self, return_value, input_lookup_data, tick_count, update_program_counter = True):
        """
        Callback that executes the operations needed after returning from a function call.
        """

        logging.debug("Called on_function_return()")

        self._init_function_call_lookup()
        
        try:
            # callback for registers
            self.register_file.on_function_return()

            # deallocate stack; ebp is direct address, without prefix
            try:
                self.memory.stack.deallocate(self.register_file.ebp, False, True)
            except MemoryException:
                # stack has not grown
                pass

            # pop ebp
            ebp = self.memory.stack.pop(self.memory.address_dimension)
            self.register_file.ebp = ebp

            # pop pc
            pc = self.memory.stack.pop(self.memory.address_dimension)
            self.register_file.pc.restore(pc)

            self.register_file.pc._pc_tracking.pop()

            # pop parameters
            function_args = self.current_instruction.function_args
            params_count = len(function_args)
            saved_params_number = min(params_count - self.register_file.param_regs_count, 0)

            params_count -= 1

            for i in range(params_count, params_count-saved_params_number, -1):
                arg = self.function_args[i]
                arg_len = len(arg.type)
                self.memory.stack.pop(arg_len)


            # get target of returning call
            target = self.current_instruction.target

            # write return_value into target
            if target is not None:
                self.register_file.write(target.value, return_value)

            # if input lookup tracking is enabled, set lookup info
            if self.input_lookup_enabled:
                function = self.functions[self.current_instruction.name]
                
                # If returning function is an input -> set target register input lookup data
                if function.is_input:
                    lookup_data = tools.build_input_lookup_data(function.input_name, self.checkpoint_clock)
                    self.register_file.set_input_lookup(target.value, lookup_data)

                # else set target input lookup data from the one of the returned register value.
                elif target is not None:
                    self.register_file.set_input_lookup(target.value, input_lookup_data)

            # increment pc and clock
            self.on_run(tick_count, update_program_counter)

        # end of program reached (pop will fail)
        except (MemoryException, IndexError):
            # set pc to len of main
            self.register_file.pc.update(self._main_function_name, self._main_function_len)

            # set return value
            self.main_return_value = return_value

            # increment clock
            self.on_run(tick_count, False)
        

    def on_branch(self, label, basic_block_id, tick_count):
        """
        Callback that executes the operations needed to perform the branch operation, which updates program counter and last_basic_block.
        """

        logging.debug("Called on_branch()")

        self.register_file.last_basic_block = basic_block_id
        
        # get current function name to retrieve the instruction_id corresponding to the given label
        current_function_name = self.register_file.pc.function_name

        # get instruction_id
        next_instruction_id = self.functions[current_function_name].get_instruction_id(label)

        # update program counter
        self.register_file.pc.update(current_function_name, next_instruction_id)

        # call run's callback, without incrementing the program counter (have just been updated)
        self.on_run(tick_count, False)


    def on_run(self, tick_count, update_program_counter = True):
        """
        Callback that is executed when an instruction is run. It increments the program counter and the global_clock.
        """

        logging.debug("Called on_run()")

        # statistics
        self.stats.instruction_executed()

        self.global_clock += tick_count
        
        if update_program_counter:
            self.register_file.pc.increment_pc()
        

    @staticmethod
    def validate_program_configuration(program_configuration):
        """
        Validates the program configuration.
        """

        config = {
            'ir_function_prefix': str,
            'main_function_name': str,
            'before_restore_function_name': str,
            'after_restore_function_name': str,
            'before_checkpoint_function_name': str,
            'after_checkpoint_function_name': str,
        }

        for key in config:
            # dict key matching
            if key not in program_configuration:
                raise ConfigurationException('Invalid program configuration: key {} is missing.'.format(key))

            element = program_configuration[key]
            el_type = config[key]

            # dict value's class matching
            if not isinstance(element, el_type):
                raise ConfigurationException('Invalid program configuration for key {}: type must be {}, {} given.'.format(key, el_type.__name__, element.__class__.__name__))


    @staticmethod
    def validate_execution_depth(execution_depth):
        """
        Verifies if the user provided execution_depth is valid.
        """

        if not isinstance(execution_depth, int):
            raise ConfigurationException('Execution Depth must be a positive integer!')

        if execution_depth < 1:
            raise ConfigurationException('Execution Depth must be a positive integer!')


    @property
    def current_instruction(self):
        """
        Returns the current instruction.
        """

        logging.debug("Getting current instruction")

        pc = self.register_file.pc

        if pc.function_name not in self.functions:
            raise RuntimeException('Function {} does not exist.'.format(pc.instruction_number, pc.function_name))

        instruction = self.functions[pc.function_name].body[pc.instruction_number]

        if instruction is None:
            raise RuntimeException('Instruction #{} in function {} does not exist.'.format(pc.instruction_number, pc.function_name))

        return instruction

    def get_instruction_from_pc(self, pc):
        """
        Returns an instruction corresponding to a given program counter
        """

        logging.debug("Getting instruction with program counter {}".format(pc))

        if pc.function_name not in self.functions:
            raise RuntimeException('Function {} does not exist.'.format(pc.instruction_number, pc.function_name))

        instruction = self.functions[pc.function_name].body[pc.instruction_number]

        if instruction is None:
            raise RuntimeException('Instruction #{} in function {} does not exist.'.format(pc.instruction_number, pc.function_name))

        return instruction
    
    
    @property
    def program_end_reached(self):
        """
        Returns if the end of the program has been reached.
        """

        pc = self.register_file.pc

        # given a main of 5 instructions (0 to 4), end of program is reached if pc is on instruction 5 (with doesn't exists)
        return self.force_stop or pc.function_name == self._main_function_name and pc.instruction_number >= self._main_function_len


    def run_step(self):
        """
        Runs the current instruction.
        """

        logging.debug("Called run_step()")

        if self.program_end_reached:

            if self.force_stop:
                raise StopException('Stop by user')

            raise RuntimeException('Program ended with return value {}'.format(self.main_return_value))

        instruction = self.current_instruction

        logging.info('({}) Running instruction {}.'.format(self.register_file.pc, instruction.instruction_type))

        instruction.run()
    
    def reset(self):
        """
        Performs the CPU reset operations.
        """

        self.memory.reset()
        self.register_file.reset(self._main_function_name)
        self._init_function_call_lookup()
        self.trigger_reset_and_restore = False
        self.global_clock = 0
        self.checkpoint_clock = 0
        self.main_return_value = None
        self.force_stop = False


    def handle_stop_request(self, anomaly):
        """
        Stops the analysis if stop_on_first_anomaly is set to True, accordingly to the user input.
        """

        if not self.stop_on_first_anomaly:
            return

        print("An anomaly has been found:\n{}\nContinue? [y/N]".format(anomaly))

        res = input()

        if res != 'y':
            raise StopAnomalyFoundException()
