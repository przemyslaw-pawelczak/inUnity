import os
from datetime import datetime

from ScEpTIC import llvmir_parser, tools
from ScEpTIC.exceptions import ConfigurationException, StopAnomalyFoundException, StopException

from .intermittent_executor import configurator
from .intermittent_executor import interruption_managers
from .intermittent_executor.checkpoint_manager import CheckpointManager
from .io.input import InputManager
from .io.output import OutputManager, OutputSkeleton
from .vmstate import VMState

class VM:
    """
    Execution environment for LLVM IR code
    """

    def __init__(self, config):
        # loads the prebuilt system config, if is different from custom
        configurator.load_prebuilt_config(config)

        self._initialize_test_vars(config)

        self.parsed = llvmir_parser.parse_file(config.file, config.PARSER_LOG_LEVEL, config.LOG_SECTION_CONTENT)

        self.state = VMState(config.program_configuration, config.register_file_configuration, config.memory_configuration, config.execution_depth)
        self.state.stop_on_first_anomaly = config.stop_on_first_anomaly

        self.state.stats.test_name = self.test_name

        self.checkpoint_manager = CheckpointManager(config.checkpoint_mechanism_configuration, self.state)
        self.checkpoint_manager.process_checkpoint_routines(self.parsed['function_definitions'], self.parsed['function_declarations'])
        
        self.state.init_gst(self.parsed['global_vars'])
        self.state.init_code(self.parsed['function_definitions'], self.parsed['function_declarations'])


    def _initialize_test_vars(self, config):
        if 'save_test_results' not in config.__dict__:
            raise ConfigurationException('Variable save_test_results not found in configuration!')
            
        elif not isinstance(config.save_test_results, bool):
            raise ConfigurationException('Variable save_test_results must be a bool, {} given.'.format(config.save_test_results.__class__.__name__))
        
        if 'stop_on_first_anomaly' not in config.__dict__:
            raise ConfigurationException('Variable stop_on_first_anomaly not found in configuration!')
            
        elif not isinstance(config.stop_on_first_anomaly, bool):
            raise ConfigurationException('Variable stop_on_first_anomaly must be a bool, {} given.'.format(config.stop_on_first_anomaly.__class__.__name__))

        if 'save_dir' not in config.__dict__:
            raise ConfigurationException('Variable save_dir not found in configuration!')
            
        elif not isinstance(config.save_dir, str):
            raise ConfigurationException('Variable save_dir must be a str, {} given.'.format(config.save_dir.__class__.__name__))

        if 'save_llvmir_code' not in config.__dict__:
            raise ConfigurationException('Variable save_llvmir_code not found in configuration!')
            
        elif not isinstance(config.save_llvmir_code, bool):
            raise ConfigurationException('Variable save_llvmir_code must be a bool, {} given.'.format(config.save_llvmir_code.__class__.__name__))

        if 'save_vm_state' not in config.__dict__:
            raise ConfigurationException('Variable save_vm_state not found in configuration!')
            
        elif not isinstance(config.save_vm_state, bool):
            raise ConfigurationException('Variable save_vm_state must be a bool, {} given.'.format(config.save_vm_state.__class__.__name__))

        if 'run_continuous' not in config.__dict__:
            raise ConfigurationException('Variable run_continuous not found in configuration!')

        elif not isinstance(config.run_continuous, bool):
            raise ConfigurationException('Variable run_continuous must be a bool, {} given.'.format(config.run_continuous.__class__.__name__))

        if 'run_locate_memory_test' not in config.__dict__:
            raise ConfigurationException('Variable run_locate_memory_test not found in configuration!')

        elif not isinstance(config.run_locate_memory_test, bool):
            raise ConfigurationException('Variable run_locate_memory_test must be a bool, {} given.'.format(config.run_locate_memory_test.__class__.__name__))

        if 'run_evaluate_memory_test' not in config.__dict__:
            raise ConfigurationException('Variable run_evaluate_memory_test not found in configuration!')

        elif not isinstance(config.run_evaluate_memory_test, bool):
            raise ConfigurationException('Variable run_evaluate_memory_test must be a bool, {} given.'.format(config.run_evaluate_memory_test.__class__.__name__))

        if 'run_input_consistency_test' not in config.__dict__:
            raise ConfigurationException('Variable run_input_consistency_test not found in configuration!')

        elif not isinstance(config.run_input_consistency_test, bool):
            raise ConfigurationException('Variable run_input_consistency_test must be a bool, {} given.'.format(config.run_input_consistency_test.__class__.__name__))

        if 'run_output_profiling' not in config.__dict__:
            raise ConfigurationException('Variable run_output_profiling not found in configuration!')

        elif not isinstance(config.run_output_profiling, bool):
            raise ConfigurationException('Variable run_output_profiling must be a bool, {} given.'.format(config.run_output_profiling.__class__.__name__))

        if 'run_profiling' not in config.__dict__:
            raise ConfigurationException('Variable run_profiling not found in configuration!')

        elif not isinstance(config.run_profiling, bool):
            raise ConfigurationException('Variable run_profiling must be a bool, {} given.'.format(config.run_profiling.__class__.__name__))
        
        if 'test_name' not in config.__dict__:
            raise ConfigurationException('Variable test_name not found in configuration!')

        elif not isinstance(config.test_name, str):
            raise ConfigurationException('Variable test_name must be a string, {} given.'.format(config.test_name.__class__.__name__))

        self.run_continuous             = config.run_continuous
        self.run_locate_memory_test     = config.run_locate_memory_test
        self.run_evaluate_memory_test   = config.run_evaluate_memory_test
        self.run_input_consistency_test = config.run_input_consistency_test
        self.run_output_profiling       = config.run_output_profiling
        self.run_profiling              = config.run_profiling
        
        self.test_name = config.test_name
        
        self.save_vm_state     = config.save_vm_state
        self.save_llvmir_code  = config.save_llvmir_code
        self.save_test_results = config.save_test_results
        self.save_dir          = os.path.join(os.getcwd(), config.save_dir, '{}_{}'.format(self.test_name, datetime.now().strftime('%Y_%m_%d_%H_%M_%S')))
            

    def _load_interruption_manager(self, module_name, class_name):
        """
        Loads a given interruption manager module.
        It also enables/disables the controls to be done during runtime operations on data, accordingly
        to the loaded module.
            - For data module enables data anomaly check
            - For input module enables input lookup anomaly check
        """

        interruption_manager = interruption_managers.get_interruption_manager(module_name, class_name)(self.state, self.checkpoint_manager)
        
        if interruption_manager.requires_static_checkpoint and self.checkpoint_manager.checkpoint_placement != 'static':
            raise ConfigurationException('Unable to run "{}, {}" test: static checkpoint placement required. System is set to {} checkpoint placement.'.format(module_name, class_name, self.checkpoint_manager.checkpoint_placement))

        self.state.do_data_anomaly_check = interruption_manager.do_data_anomaly_check
        self.state.input_lookup_enabled = interruption_manager.input_lookup_enabled
        self.state.collect_memory_trace = interruption_manager.collect_memory_trace

        return interruption_manager

    def _save_program_code(self):
        """
        If save_llvmir_code is set, saves the program code into "code" folder inside the save_dir.
        """

        if not self.save_llvmir_code or not self.save_test_results:
            return

        save_dir = os.path.join(self.save_dir, 'code')

        if os.path.exists(save_dir):
            return

        os.makedirs(save_dir, exist_ok=True)

        for function_name in self.state.functions:
            file_name = os.path.join(save_dir, '{}.txt'.format(function_name.replace(self.state.ir_function_prefix, '')))

            with open(file_name, 'w') as fp:
                fp.write('{}'.format(self.state.functions[function_name]))


    def _save_vm_state(self, name):
        """
        If save_vm_state is set, saves the simulator state after each test into a states folder.
        """

        if not self.save_vm_state or not self.save_test_results:
            return

        save_dir = os.path.join(self.save_dir, 'states')

        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)

        save_file = os.path.join(save_dir, '{}.txt'.format(name))

        with open(save_file, 'w') as fp:
            fp.write(self.get_visual_dump())


    def reset(self):
        """
        Resets the whole status of the simulator.
        """

        self.checkpoint_manager.reset()
        self.state.reset()
        self.state.memory.force_nvm_reset()
        self.state.stats.reset()


    def _get_stop_info(self):
        """
        Returns stop information
        """

        pc_stop_at = ''
        space = '  '
        for pc in self.state.register_file.pc._pc_tracking:
            pc_stop_at += '{}{} -> {}\n'.format(space, pc['function_name'], pc['instruction_number'])
            space += ' '*4

        pc_stop_at += '{}{}\n'.format(space, self.state.register_file.pc)

        return pc_stop_at, self.state.global_clock


    def stop_current_test(self):
        """
        Stops the current test
        """

        self.state.force_stop = True

        pc_stop_at, clock = self._get_stop_info()
        self.state.stats.stop_at(pc_stop_at, clock)


    def run_test(self, module_name, class_name):
        """
        Runs completely a test, given the test module (interruption manager)
        """

        print('Running {} test using {}'.format(module_name, class_name))
        
        interruption_manager = self._load_interruption_manager(module_name, class_name)

        self._save_program_code()
        self.reset_anomalies()
        self.reset_profiling()
        self.reset()

        while not self.state.program_end_reached:
            try:
                if interruption_manager.intermittent_execution_required():
                    interruption_manager.run_with_intermittent_execution()
                    
                else:
                    self.state.run_step()

            except StopAnomalyFoundException:
                pc_stop_at, clock = self._get_stop_info()
                self.state.stats.stop_at(pc_stop_at, clock, True)
                break

            except StopException:
                pc_stop_at, clock = self._get_stop_info()
                self.state.stats.stop_at(pc_stop_at, clock)
                break
                
        if self.save_test_results:

            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir, exist_ok=True)

            anomalies_file_name = os.path.join(self.save_dir, '{}_anomalies.txt'.format(module_name))
            profiling_file_name = os.path.join(self.save_dir, '{}_profiling.txt'.format(module_name))

        else:
            anomalies_file_name = None
            profiling_file_name = None

        self.get_found_anomalies(anomalies_file_name)
        
        if not self.get_profiling_info(profiling_file_name, module_name):
            self.get_observation_info(profiling_file_name)

        self._save_vm_state(module_name)

    def evaluate_run_test(self, module_name, class_name):
        """
        Estimates the number of instructions to be executed continuously
        """

        interruption_manager = self._load_interruption_manager(module_name, class_name)

        self._save_program_code()
        self.reset_anomalies()
        self.reset_profiling()
        self.reset()

        while not self.state.program_end_reached:
            try:
                if interruption_manager.intermittent_execution_required():
                    self.state.run_step()
                    self.state.evaluation_metrics.checkpoint_executed()
                else:
                    self.state.run_step()

            except StopAnomalyFoundException:
                pc_stop_at, clock = self._get_stop_info()
                self.state.evaluation_metrics.stop_at(pc_stop_at, clock, True)
                break

            except StopException:
                pc_stop_at, clock = self._get_stop_info()
                self.state.evaluation_metrics.stop_at(pc_stop_at, clock)
                break
        
        print(self.state.evaluation_metrics)



    def run_tests(self):
        """
        Runs the tests configured in the config file.
        """

        if self.run_continuous:
            self.run_test('base', 'InterruptionManager')

        if self.run_evaluate_memory_test:
            self.run_test('memory_evaluate', 'EvaluateMemoryAnomaliesInterruptionManager')

        if self.run_locate_memory_test:
            self.run_test('memory_locate', 'LocateMemoryAnomaliesInterruptionManager')

        if self.run_input_consistency_test:
            self.run_test('input', 'InputInterruptionManager')

        if self.run_output_profiling:
            self.run_test('output', 'OutputInterruptionManager')

        if self.run_profiling:
            self.run_test('profiling', 'ProfilingInterruptionManager')


    def get_visual_dump(self):
        """
        Returns a visual dump of the current state of the simulator.
        """

        # registers
        retstr = '[REGISTERS]\n'+str(self.state.register_file.get_visual_dump())
        retstr += "\n"

        # stack
        retstr += '[STACK]\n'+str(self.state.memory.stack)
        retstr += self.state.memory.stack.get_visual_dump()
        retstr += "\n\n"

        # heap
        retstr += '[HEAP]\n'+str(self.state.memory.heap)
        retstr += self.state.memory.heap.get_visual_dump()
        retstr += "\n"

        # gst
        retstr += '[GST]\n'+self.state.memory.gst.get_visual_dump()
        retstr += "\n\n"

        # input table
        retstr += '[INPUT TABLE]\n{}\n\n'.format(tools.fancy_dict_to_str(InputManager.input_table))

        # output table
        retstr += '[OUTPUT TABLE]\n{}\n\n'.format(tools.fancy_dict_to_str(OutputManager.output_table))

        # output idempotency
        retstr += '[OUTPUT IDEMPOTENCY]\n{}\n\n'.format(tools.fancy_dict_to_str(OutputManager.get_measured_idempotency()))
        
        # global clock
        retstr += 'Global Clock: {}\n\n'.format(self.state.global_clock)

        # stats
        retstr += '[Stats]\n {}\n\n'.format(str(self.state.stats).replace('\n', '\n '))
        
        return retstr

    def get_found_anomalies(self, outfile = None):
        """
        Prints out the found anomalies. If an outfile is specified, such information is written inside it.
        """

        if len(self.state.anomalies) == 0:
            return None

        retval = "Found anomalies: {}\n\n".format(len(self.state.anomalies))

        for anomaly in self.state.anomalies:
            retval += '{}\n'.format(anomaly)

        if outfile is None:
            print(retval)

        else:
            with open(outfile, 'w') as fp:
                fp.write(retval)
        

    def get_profiling_info(self, outfile = None, module_name = ''):
        """
        Prints out the gethered profiling information. If an outfile is specified, such information is written inside it.
        """

        if len(self.state.profiling) == 0:
            return False

        if module_name == 'output':
            return self.get_output_profiling_info(outfile)
        
        retval = 'Observed clock cycles: {}\n\n'.format(len(self.state.profiling))
        spaces = ' ' * 4

        for clock_id in sorted(self.state.profiling):
            checkpoint_pc = self.state.checkpoint_clock_pc_maps[clock_id]
            retval += 'Checkpoint: {}Global clock: {}\n\n'.format(checkpoint_pc.resolve(), clock_id)

            runs = self.state.profiling[clock_id]

            for run_id in sorted(runs):
                if run_id == 0:
                    retval += '{}Normal execution:\n'.format(spaces)
                else:
                    retval += '{}#{} power failure generated:\n'.format(spaces, run_id)

                run = runs[run_id]
                
                for io in run:
                    io_str = str(io).replace('\n', '\n{}'.format(spaces*3))
                    retval += '{}{}\n'.format(spaces*2, io_str)

                retval += '\n'

            retval += '\n'

        if outfile is None:
            print(retval)

        else:
            with open(outfile, 'w') as fp:
                fp.write(retval)

        return True

    def get_output_profiling_info(self, outfile = None):
        if len(self.state.profiling) == 0:
            return False
        
        retval = ''

        spaces = ' ' * 4

        for clock_id in sorted(self.state.profiling):
            checkpoint_pc = self.state.checkpoint_clock_pc_maps[clock_id]
            retval += 'Checkpoint: {}\n'.format(checkpoint_pc.resolve(), clock_id)

            outs = self.state.profiling[clock_id]

            for out in outs:
                tracking = outs[out]
                
                if len(tracking) == 0:
                    continue

                retval += '{}Output {}\n'.format(spaces, OutputSkeleton.output_names[out.replace(self.state.ir_function_prefix, '')])

                
                for track in tracking:
                    out_str = str(track).replace('\n', '\n{}'.format(spaces*3))
                    retval += '{}{}\n'.format(spaces*2, out_str)

                retval += '\n'

            retval += '\n'

        if outfile is None:
            print(retval)

        else:
            with open(outfile, 'w') as fp:
                fp.write(retval)

        return True


    def get_observation_info(self, outfile = None):
        """
        Prints out the gethered profiling information. If an outfile is specified, such information is written inside it.
        """

        if len(self.state.observations) == 0:
            return False

        retval = ''

        for first_checkpoint in self.state.observations:
            retval += 'Checkpoint: {}\n'.format(first_checkpoint.resolve())

            for second_checkpoint in self.state.observations[first_checkpoint]:
                try:
                    second_checkpoint_str = second_checkpoint.resolve()
                except IndexError:
                    second_checkpoint_str = 'Program End\n'

                retval += '{}End checkpoint: {}'.format(' '*4, second_checkpoint_str)
                retval += '{}Input access models:\n{}'.format(' '*6, tools.fancy_dict_to_str(self.state.observations[first_checkpoint][second_checkpoint], 7))

                retval += '\n'
                
            retval += '\n'

        if outfile is None:
            print(retval)

        else:
            with open(outfile, 'w') as fp:
                fp.write(retval)

        return True


    def reset_anomalies(self):
        """
        Resets the found anomalies.
        """

        self.state.anomalies = []

    def reset_profiling(self):
        """
        Resets the gathered profiling information.
        """

        self.state.anomalies = []
