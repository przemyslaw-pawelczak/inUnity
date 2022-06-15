import copy
import gc
import logging

from ScEpTIC.AST.elements.instructions.other_operations import CallOperation
from ScEpTIC.AST.elements.instructions.termination_instructions import ReturnOperation
from ScEpTIC.emulator.io.output import OutputManager
from ScEpTIC.exceptions import ConfigurationException, MemoryException

class CheckpointManager:
    """
    Manages checkpoint and restore operations
    """

    def __init__(self, config, vmstate):
        self.validate_configuration(config)

        positions = vmstate.memory.memory_positions

        self.checkpoint_placement = config['checkpoint_placement']
        self.routine_names = {'checkpoint': vmstate.ir_function_prefix + config['checkpoint_routine_name'], 'restore': vmstate.ir_function_prefix + config['restore_routine_name']}
        
        # set checkpoint/restore routines to be ignored on function call
        CallOperation.ignore.append(self.routine_names['checkpoint'])
        CallOperation.ignore.append(self.routine_names['restore'])

        self.restore_register_file = config['restore_register_file']
        self.restore_stack = config[positions['stack']]['restore_stack']
        self.restore_heap  = config[positions['heap']]['restore_heap']
        self.restore_sram_gst = config['sram']['restore_gst'] & ('sram' in positions['gst'])
        self.restore_nvm_gst = config['nvm']['restore_gst'] & ('nvm' in positions['gst'])

        self.restore_environment = config['environment']

        self.stack_position = positions['stack']

        self.vmstate = vmstate

        self.stop_on_power_interrupt = config['on_dynamic_voltage_alert'] == 'stop'

        self.reset()


    def reset(self):
        """
        Resets the saved dump and checkpoint
        """

        self.checkpoint = {'register_file': None, 'reg_saving_pool': None, 'stack': None, 'heap': None, 'sram_gst': None, 'nvm_gst': None, 'stack_top_address': None, 'global_clock': 0, 'function_call_lookup': None, 'output': None}
        self.dump = {'register_file': None, 'reg_saving_pool': None, 'stack': None, 'heap': None, 'sram_gst': None, 'nvm_gst': None, 'global_clock': 0, 'function_call_lookup': None, 'output': None}


    def process_checkpoint_routines(self, functions, declarations):
        """
        If dynamic checkpoint mechanisms: removes all references to the checkpoint and restore routines (if any).
        If static checkpoint mechanisms: removes all references to restore routine and removes target from checkpoint routine calls.

        NB: Checkpoint routine is considered just as a marker to verify when interrupt and test the execution.
        """

        # remove declaration of checkpoint routine
        if self.routine_names['checkpoint'] in declarations:
            del declarations[self.routine_names['checkpoint']]

        # remove declaration of restore
        if self.routine_names['restore'] in declarations:
            del declarations[self.routine_names['restore']]

        # parse each function and remove restore routine (usually is at the start of the main)
        for name in functions:
            function = functions[name]

            i = 0

            while i < len(function.body):
                instruction = function.body[i]
                
                # if is a restore operation, remove it (both in static and dynamic checkpoint, since it must be at the top)
                if isinstance(instruction, CallOperation) and instruction.name == self.routine_names['restore']:

                    # preserve label of the instruction to be removed
                    if instruction.label is not None:
                        function.body[i+1].label = copy.deepcopy(instruction.label)

                    del function.body[i]

                # if is a checkpoint operation
                elif isinstance(instruction, CallOperation) and instruction.name == self.routine_names['checkpoint']:

                    # if dynamic mechanism, remove it.
                    if self.checkpoint_placement == 'dynamic':

                        # preserve label
                        if instruction.label is not None:
                            function.body[i+1].label = copy.deepcopy(instruction.label)
                    
                        del function.body[i]

                    # if static mechanism, remove its target and continue
                    else:
                        function.body[i].target = None
                        i += 1

                else:
                    i += 1

            # update function labels
            function.update_labels()

            # remove from internal calls the restore and checkpoint functions, so to not consider them during registers allocation
            function._remove_from_calls(self.routine_names['restore'])
            function._remove_from_calls(self.routine_names['checkpoint'])

    def get_simple_dump(self):
        """
        Returns a dump of register file, stack, heap and gst.
        """

        dump = {}
        dump['register_file'] = self.vmstate.register_file.dump()
        dump['stack'] = self.vmstate.memory.stack.dump()
        dump['heap'] = self.vmstate.memory.heap.dump()
        
        sram_gst = self.vmstate.memory.gst._get_gst_from_ram_name('SRAM')
        dump['sram_gst'] = sram_gst.dump() if sram_gst is not None else None
        
        nvm_gst = self.vmstate.memory.gst._get_gst_from_ram_name('NVM')
        dump['nvm_gst'] = nvm_gst.dump() if nvm_gst is not None else None

        dump['output'] = OutputManager.dump()
        
        # stats
        self.vmstate.stats.dump_executed()

        return dump

    def do_checkpoint(self):
        """
        Performs a checkpoint of the selected elements and dumps the whole vm state.
        The saved checkpoint is the one restored by the do_restore routine.
        The vm state is saved for comparisons with the obtained status after a restore.
        """

        logging.info('[CheckpointManager] Saving checkpoint.')

        self._inject_function_call('before_checkpoint')

        # save register file
        del self.dump['register_file']
        del self.dump['reg_saving_pool']
        self.dump['register_file'] = self.vmstate.register_file.dump()
        self.dump['reg_saving_pool'] = copy.deepcopy(self.vmstate.reg_saving_pool)

        if self.restore_register_file:
            del self.checkpoint['register_file']
            self.checkpoint['register_file'] = copy.deepcopy(self.dump['register_file'])
            # Stack Top Address = ESP, saved in the stack but is a register.
            del self.checkpoint['stack_top_address']
            del self.checkpoint['reg_saving_pool']
            self.checkpoint['stack_top_address'] = copy.deepcopy(self.vmstate.memory.stack.top_address)
            self.checkpoint['reg_saving_pool'] = copy.deepcopy(self.vmstate.reg_saving_pool)

        # save stack
        del self.dump['stack']
        self.dump['stack'] = self.vmstate.memory.stack.dump()

        if self.restore_stack:
            del self.checkpoint['stack']
            self.checkpoint['stack'] = copy.deepcopy(self.dump['stack'])

        # save heap
        del self.dump['heap']
        self.dump['heap'] = self.vmstate.memory.heap.dump()

        if self.restore_heap:
            del self.checkpoint['heap']
            self.checkpoint['heap'] = copy.deepcopy(self.dump['heap'])

        # save sram gst
        sram_gst = self.vmstate.memory.gst._get_gst_from_ram_name('SRAM')

        if sram_gst is not None:
            del self.dump['sram_gst']
            self.dump['sram_gst'] = sram_gst.dump()

            if self.restore_sram_gst:
                del self.checkpoint['sram_gst']
                self.checkpoint['sram_gst'] = copy.deepcopy(self.dump['sram_gst'])

        # save nvm gst
        nvm_gst = self.vmstate.memory.gst._get_gst_from_ram_name('NVM')

        if nvm_gst is not None:
            del self.dump['nvm_gst']
            self.dump['nvm_gst'] = nvm_gst.dump()

            if self.restore_nvm_gst:
                del self.checkpoint['nvm_gst']
                self.checkpoint['nvm_gst'] = copy.deepcopy(self.dump['nvm_gst'])

        del self.checkpoint['global_clock']
        self.checkpoint['global_clock'] = self.vmstate.global_clock

        del self.dump['global_clock']
        self.dump['global_clock'] = self.vmstate.global_clock

        # save function call lookup
        del self.checkpoint['function_call_lookup']
        self.checkpoint['function_call_lookup'] = copy.deepcopy(self.vmstate.function_call_lookup)
        del self.dump['function_call_lookup']
        self.dump['function_call_lookup'] = copy.deepcopy(self.vmstate.function_call_lookup)

        # stats
        self.vmstate.stats.checkpoint_executed()

        self._inject_function_call('after_checkpoint')

        if self.restore_environment:
            del self.checkpoint['output']
            self.checkpoint['output'] = OutputManager.dump()

        del self.dump['output']
        self.dump['output'] = OutputManager.dump()

        gc.collect()


    def do_restore(self):
        """
        Restores the previously taken checkpoint.
        """

        logging.info('[CheckpointManager] Restoring checkpoint.')

        self._inject_function_call('before_restore')

        # restore stack, if its checkpoint is present
        if self.checkpoint['stack'] is not None:
            self.vmstate.memory.stack.restore(self.checkpoint['stack'])

        # restore register saving pool used by register allocation to track registers
        if self.checkpoint['reg_saving_pool'] is not None:
            self.vmstate.reg_saving_pool = copy.deepcopy(self.checkpoint['reg_saving_pool'])

        # restore register file, if its checkpoint is present
        if self.checkpoint['register_file'] is not None:
            self.vmstate.register_file.restore(self.checkpoint['register_file'])

            # if stack in sram, the checkpoint will contain only the real portion of the stack
            # so "real" memory zeroing is required.
            if self.stack_position == 'sram':

                # in the first growing of the stack, no memory cell is exceeding top_address
                try:
                    self.vmstate.memory.stack._deallocate(self.checkpoint['stack_top_address'], False, True)

                except MemoryException:
                    pass

            # if stack not restored, restore ESP (is a relative address of the stack)
            if self.checkpoint['stack'] is None:
                # in the first growing of the stack, no memory cell is exceeding top_address
                try:
                    self.vmstate.memory.stack.deallocate(self.checkpoint['stack_top_address'], False, True)

                except MemoryException:
                    pass

        # restore heap, if its checkpoint is present
        if self.checkpoint['heap'] is not None:
            self.vmstate.memory.heap.restore(self.checkpoint['heap'])

        # restore sram_gst, if its checkpoint is present
        if self.checkpoint['sram_gst'] is not None:
            self.vmstate.memory.sram.gst.restore(self.checkpoint['sram_gst'])

        # restore nvm_gst, if its checkpoint is present
        if self.checkpoint['nvm_gst'] is not None:
            self.vmstate.memory.nvm.gst.restore(self.checkpoint['nvm_gst'])

        # restore global_clock, if its checkpoint is present
        if self.checkpoint['global_clock'] > 0:
            self.vmstate.global_clock = self.checkpoint['global_clock']

        # restore function call's stack lookup
        if self.checkpoint['function_call_lookup'] is not None:
            self.vmstate.function_call_lookup = copy.deepcopy(self.checkpoint['function_call_lookup'])

        if self.restore_environment:
            OutputManager.restore(self.checkpoint['output'])

        # stats
        self.vmstate.stats.checkpoint_restored()
        
        self._inject_function_call('after_restore')


    def restore_dump(self):
        """
        Restores the previously taken dump, to make memory consistent again.
        """

        logging.info('[CheckpointManager] Restoring memory state to a consistent one.')

        # restore register file, if its dump is present
        if self.dump['register_file'] is not None:
            self.vmstate.register_file.restore(self.dump['register_file'])

        # restore register saving pool used by register allocation to track registers
        if self.dump['reg_saving_pool'] is not None:
            self.vmstate.reg_saving_pool = copy.deepcopy(self.dump['reg_saving_pool'])

        # restore stack, if its dump is present
        if self.dump['stack'] is not None:
            self.vmstate.memory.stack.restore(self.dump['stack'])

        # restore heap, if its dump is present
        if self.dump['heap'] is not None:
            self.vmstate.memory.heap.restore(self.dump['heap'])

        # restore sram_gst, if its dump is present
        if self.dump['sram_gst'] is not None:
            self.vmstate.memory.sram.gst.restore(self.dump['sram_gst'])

        # restore nvm_gst, if its dump is present
        if self.dump['nvm_gst'] is not None:
            self.vmstate.memory.nvm.gst.restore(self.dump['nvm_gst'])

        # restore global_clock, if its dump is present
        if self.dump['global_clock'] > 0:
            self.vmstate.global_clock = self.dump['global_clock']

        # restore function call's stack lookup
        if self.dump['function_call_lookup'] is not None:
            self.vmstate.function_call_lookup = copy.deepcopy(self.dump['function_call_lookup'])

        # restore output table
        if self.dump['output'] is not None:
            OutputManager.restore(self.dump['output'])

        # stats
        self.vmstate.stats.dump_restored()
        

    def get_vm_state_diff(self):
        """
        Compares the vm state with the vm dump taken during the checkpoint.
        It returns a list containing the memory section names that differs.
        """

        comparations = {
            'register_file': self.vmstate.register_file == self.dump['register_file'],
            'stack': self.vmstate.memory.stack == self.dump['stack'],
            'heap': self.vmstate.memory.heap == self.dump['heap'],
            'sram_gst': self.vmstate.memory.gst._get_gst_from_ram_name('SRAM') == self.dump['sram_gst'],
            'nvm_gst': self.vmstate.memory.gst._get_gst_from_ram_name('NVM') == self.dump['nvm_gst'],
            'global_clock': self.vmstate.global_clock == self.dump['global_clock'],
            'environment': OutputManager.output_table == self.dump['output']
        }

        for name in list(comparations.keys()):
            # remove memory sections names which are not changed.
            if comparations[name]:
                del comparations[name]

        return list(comparations.keys())


    def get_vm_state_diff_elements(self):
        """
        Returns a dictionary containing the differences for each memory component between the current state and the saved dump.
        """

        if self.vmstate.global_clock != self.dump['global_clock']:
            global_clock_diff = [{'element': 'global_clock', 'dump_value': self.dump['global_clock'], 'current_value': self.vmstate.global_clock}]

        else:
            global_clock_diff = []

        diffs = {
            'register_file': self.vmstate.register_file.diff(self.dump['register_file']),
            'stack': self.vmstate.memory.stack.diff(self.dump['stack']),
            'heap': self.vmstate.memory.heap.diff(self.dump['heap']),
            'sram_gst': self.vmstate.memory.gst._get_gst_from_ram_name('SRAM').diff(self.dump['sram_gst']),
            'nvm_gst': self.vmstate.memory.gst._get_gst_from_ram_name('NVM').diff(self.dump['nvm_gst']),
            'global_clock': global_clock_diff,
            'environment': OutputManager.diff(self.dump['output'])
        }

        return diffs



    @staticmethod
    def validate_configuration(configuration):
        """
        Validates the checkpoint configuration. If an error is found, a ConfigurationException is raised.
        """

        config = {
            'checkpoint_placement': str,
            'on_dynamic_voltage_alert': str,
            'checkpoint_routine_name': str,
            'restore_routine_name': str,
            'restore_register_file': bool,
            'sram': {'restore_stack': bool, 'restore_heap': bool, 'restore_gst': bool},
            'nvm': {'restore_stack': bool, 'restore_heap': bool, 'restore_gst': bool},
            'environment': bool
        }

        domains = {
            'checkpoint_placement': ['dynamic', 'static'],
            'on_dynamic_voltage_alert': ['continue', 'stop']
        }

        # keys must match
        for key in config:
            if key not in configuration:
                raise ConfigurationException('Invalid memory configuration: key {} is missing.'.format(key))

            sub_conf = config[key]
            sub_mem_conf = configuration[key]

            if isinstance(sub_conf, dict):
                # keys of subdictionary must match
                for sub_key in sub_conf:
                    if sub_key not in sub_mem_conf:
                        raise ConfigurationException('Invalid checkpoint mechanism configuration: subkey {} of key {} is missing.'.format(sub_key, key))

                    sub_type = sub_conf[sub_key]
                    
                    # types must match
                    if not isinstance(sub_mem_conf[sub_key], sub_type):
                        raise ConfigurationException('Invalid checkpoint mechanism configuration for subkey {} of key {}: type must be {}, {} given.'.format(sub_key, key, sub_type.__name__, sub_mem_conf[sub_key].__class__.__name__))
            
            elif not isinstance(sub_mem_conf, sub_conf):
                raise ConfigurationException('Invalid checkpoint mechanism configuration for key {}: type must be {}, {} given.'.format(key, sub_conf.__name__, sub_mem_conf.__class__.__name__))

        if not configuration['restore_register_file']:
            raise ConfigurationException('NVM CPUs not supported! Registers saving must be enabled!')

        for i in domains:
            if configuration[i] not in domains[i]:
                raise ConfigurationException('Invalid value of {} ({}). It must be in {}'.format(i, config[i], domains[i]))


    def _inject_function_call(self, name):
        """
        Inject a custom function call
        """

        if name not in self.vmstate.custom_exec_names:
            return

        function_name = self.vmstate.custom_exec_names[name]['name']

        # correct return operation(s) of the injected function
        ret_ops = self.vmstate.custom_exec_names[name]['ret_ops']

        pc = self.vmstate.register_file.pc.save()

        # inject PC
        self.vmstate.register_file.pc.update(function_name, 0)

        while self.vmstate.current_instruction not in ret_ops:
            self.vmstate.run_step()
        
        # restore PC
        self.vmstate.register_file.pc.restore(pc)


    def do_dump(self):
        """
        Performs a dump of the vm state
        """

        del self.dump['register_file']
        del self.dump['reg_saving_pool']
        del self.dump['stack']
        del self.dump['heap']
        del self.dump['sram_gst']
        del self.dump['nvm_gst']
        del self.dump['global_clock']
        del self.dump['function_call_lookup']
        del self.dump['output']
        gc.collect()

        # save register file
        self.dump['register_file'] = self.vmstate.register_file.dump()
        self.dump['reg_saving_pool'] = copy.deepcopy(self.vmstate.reg_saving_pool)

        # save stack
        self.dump['stack'] = self.vmstate.memory.stack.dump()

        # save heap
        self.dump['heap'] = self.vmstate.memory.heap.dump()

        # save sram gst
        sram_gst = self.vmstate.memory.gst._get_gst_from_ram_name('SRAM')
        self.dump['sram_gst'] = sram_gst.dump()

        if sram_gst is not None:
            self.dump['sram_gst'] = sram_gst.dump()
        else:
            self.dump['sram_gst'] = None

        # save nvm gst
        nvm_gst = self.vmstate.memory.gst._get_gst_from_ram_name('NVM')

        if nvm_gst is not None:
            self.dump['nvm_gst'] = nvm_gst.dump()
        else:
            self.dump['nvm_gst'] = None

        self.dump['global_clock'] = self.vmstate.global_clock

        # save function call lookup
        self.dump['function_call_lookup'] = copy.deepcopy(self.vmstate.function_call_lookup)

        self.dump['output'] = OutputManager.dump()
