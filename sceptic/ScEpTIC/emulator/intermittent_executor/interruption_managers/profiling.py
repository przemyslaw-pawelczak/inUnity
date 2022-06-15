import copy
import logging

from collections import defaultdict

from ScEpTIC.AST.elements.instructions.other_operations import CallOperation
from ScEpTIC.AST.elements.instructions.termination_instructions import ReturnOperation
from ScEpTIC.emulator.intermittent_executor.profiling import ProfilingReset, RunInfo, ProfilingLog
from ScEpTIC.emulator.io.input import InputManager, InputSkeleton
from ScEpTIC.emulator.io.output import OutputManager, OutputSkeleton
from ScEpTIC.exceptions import RuntimeException, StopException, MemoryException

from .base import InterruptionManager


class ProfilingInterruptionManager(InterruptionManager):
    """
    Interruption manager for profiling intermittent executions
    """

    requires_static_checkpoint = False

    def __init__(self, vmstate, checkpoint_manager):
        super().__init__(vmstate, checkpoint_manager)
        self.output_functions = []
        self.input_functions = []

        self.is_dynamic = self.checkpoint_manager.checkpoint_placement == 'dynamic'
        
        for key in OutputSkeleton.output_functions:
            function_name = '{}{}'.format(self.vmstate.ir_function_prefix, OutputSkeleton.output_functions[key])
            self.output_functions.append(function_name)

        for key in InputSkeleton.input_functions:
            function_name = '{}{}'.format(self.vmstate.ir_function_prefix, InputSkeleton.input_functions[key])
            self.input_functions.append(function_name)

    def _execution_condition(self):
        """
        Checks if we are inside the current checkpoint interval
        """

        if self.vmstate.program_end_reached:
            return False

        current_instruction = self.vmstate.current_instruction

        if isinstance(current_instruction, CallOperation) and current_instruction.name == self.checkpoint_manager.routine_names['checkpoint']:
            return False

        return True


    def intermittent_execution_required(self):
        return True


    def _is_call_to_output(self):
        current_instruction = self.vmstate.current_instruction
        return isinstance(current_instruction, CallOperation) and current_instruction.name in self.output_functions


    def run_with_intermittent_execution(self):
        logging.info('[ProfilingInterruptionManager] Running {} in intermittent execution scenario.'.format(self.vmstate.register_file.pc))

        # could be also the first instruction of the program
        checkpoint_pc = copy.deepcopy(self.vmstate.register_file.pc)
        checkpoint_clock = self.vmstate.global_clock
        self.vmstate.checkpoint_clock_pc_maps[checkpoint_clock] = copy.deepcopy(checkpoint_pc)

        # Only after first instruction of the program
        if self.vmstate.global_clock > 0:
            current_instruction = self.vmstate.current_instruction

            if not isinstance(current_instruction, CallOperation) or current_instruction.name != self.checkpoint_manager.routine_names['checkpoint']:
                raise RuntimeException('[ProfilingInterruptionManager] Checkpoint operation required. {} given.'.format(current_instruction.__class__.__name__))

            # PC -> checkpoint. skip PC, since the simulator executes it.
            self.vmstate.register_file.pc.increment_pc()
            self.vmstate.global_clock += 1
    
        # do checkpoint
        self.checkpoint_manager.do_checkpoint()

        force_stop = False

        power_failures = 0

        tracking = defaultdict(list)

        ProfilingLog.tracking = tracking
        ProfilingLog.power_failures = power_failures

        while self._execution_condition():

            current_instruction = self.vmstate.current_instruction
            
            # if it is a call operation, can be an input/output operation
            if isinstance(current_instruction, CallOperation):

                io_type = None

                if current_instruction.name in self.output_functions:
                    io_type = 'OUTPUT'

                elif current_instruction.name in self.input_functions:
                    io_type = 'INPUT'

                # if is an actual I/O operation, track it.
                if io_type is not None:
                    pc = copy.deepcopy(self.vmstate.register_file.pc)
                    global_clock = self.vmstate.global_clock

                    # run i/o function
                    while not isinstance(self.vmstate.current_instruction, ReturnOperation):
                        self.vmstate.run_step()

                    # return from i/o function
                    self.vmstate.run_step()

                    function_name = current_instruction.name.replace(self.vmstate.ir_function_prefix, '')

                    if io_type == 'OUTPUT':
                        io_name = OutputSkeleton.output_names[function_name]
                        io_value = OutputManager.output_table[io_name]

                    else:
                        io_name = InputSkeleton.input_names[function_name]
                        io_value = InputManager.input_table[io_name]

                    # create tracking information
                    runinfo = RunInfo(io_type, pc, global_clock, power_failures, function_name, io_name, io_value)

                    # append tracking information
                    tracking[power_failures].append(runinfo)

                    # update variable
                    current_instruction = self.vmstate.current_instruction
            
            # if it is a profiling reset
            if isinstance(current_instruction, ProfilingReset) and current_instruction.evaluate_reset_condition(power_failures):
                power_failures += 1

                # Support for dynamic checkpoint mechanisms / Just In Time
                # Custom routine can be emulated using execute_before / execute_after functions
                if self.is_dynamic:
                    self.checkpoint_manager.do_checkpoint()

                ProfilingLog.power_failures = power_failures

                self.checkpoint_manager.do_restore()
                continue

            # run the operation. If an exception occurs, sign it and stop tracking
            try:
                self.vmstate.run_step()

                # Skip to next checkpoint interval if a stack activation record anomaly was found
                if self.has_stack_activation_record_anomalies(checkpoint_pc, False):
                    tracking[power_failures].append('Unable to continue the analysis due to a stack anomaly.')
                    self.checkpoint_manager.restore_dump()
                    force_stop = True
                    break

            except MemoryException as e:
                tracking[power_failures].append('Unable to continue the analysis due to a MemoryException: {}'.format(e))
                self.checkpoint_manager.restore_dump()
                force_stop = True
                break

        # append to global tracking info
        self.vmstate.profiling[checkpoint_clock] = tracking

        if force_stop:
            raise StopException()
