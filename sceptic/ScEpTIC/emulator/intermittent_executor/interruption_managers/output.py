import copy
import logging

from ScEpTIC.AST.elements.instructions.other_operations import CallOperation
from ScEpTIC.AST.elements.instructions.termination_instructions import ReturnOperation
from ScEpTIC.emulator.intermittent_executor.anomalies import OutputAnomaly
from ScEpTIC.emulator.intermittent_executor.profiling import RunInfo
from ScEpTIC.emulator.io.output import OutputManager, OutputSkeleton
from ScEpTIC.exceptions import RuntimeException, StopException, MemoryException

from .base import InterruptionManager


class OutputInterruptionManager(InterruptionManager):
    """
    Interruption manager for analyzing output interactions
    """

    requires_static_checkpoint = True

    def __init__(self, vmstate, checkpoint_manager):
        super().__init__(vmstate, checkpoint_manager)
        self.output_functions = []
        self.ignore_pc = []
        
        for key in OutputManager.output_idempotency_table:
            function_name = '{}{}'.format(self.vmstate.ir_function_prefix, OutputSkeleton.output_functions[key])
            self.output_functions.append(function_name)


    def intermittent_execution_required(self):
        if self.vmstate.register_file.pc in self.ignore_pc:
            return False

        return True


    def _intermittent_condition(self):
        """
        Returns if the intermittent execution test must continue.
        """

        if self.vmstate.program_end_reached:
            return False

        current_instruction = self.vmstate.current_instruction

        # if static checkpoint, stop only when another checkpoint is reached.
        if isinstance(current_instruction, CallOperation) and current_instruction.name == self.checkpoint_manager.routine_names['checkpoint']:
            return False

        return True


    def run_with_intermittent_execution(self):
        logging.info('[OutputInterruptionManager] Running {} in intermittent execution scenario.'.format(self.vmstate.register_file.pc))

        force_checkpoint = False

        current_instruction = self.vmstate.current_instruction

        # check constraint
        if not isinstance(current_instruction, CallOperation) or current_instruction.name != self.checkpoint_manager.routine_names['checkpoint']:
            if self.vmstate.global_clock == 0:
                force_checkpoint = True
            else:
                raise RuntimeException('[OutputInterruptionManager] Invalid operation {} for starting intermittent execution. Checkpoint operation required.'.format(current_instruction.__class__.__name__))

        # save checkpoint pc
        checkpoint_pc = copy.deepcopy(self.vmstate.register_file.pc)
        checkpoint_clock = self.vmstate.global_clock
        self.vmstate.checkpoint_clock_pc_maps[checkpoint_clock] = copy.deepcopy(checkpoint_pc)

        # do checkpoint
        if not force_checkpoint:
            self.vmstate.register_file.pc.increment_pc()
            self.vmstate.global_clock += 1

        self.checkpoint_manager.do_checkpoint()

        # initialize tracking dict
        tracking = {}
        reset_no = {}
        out_vals = {}

        for i in self.output_functions:
            tracking[i] = []
            reset_no[i] = 0

        resetting_out = None

        force_stop = False

        # run until the required number of runs is reached
        while self._intermittent_condition():

            if self.has_stack_activation_record_anomalies(checkpoint_pc, False):
                self.ignore_pc.append(checkpoint_pc)
                tracking[resetting_out].append('Unable to continue the analysis due to a stack anomaly.')
                self.checkpoint_manager.restore_dump()
                break

            current_instruction = self.vmstate.current_instruction

            # if is a call operation, can be an input/output operation
            if isinstance(current_instruction, CallOperation) and current_instruction.name in self.output_functions and reset_no[current_instruction.name] < 2:
                resetting_out = current_instruction.name

                pc = copy.deepcopy(self.vmstate.register_file.pc)
                global_clock = self.vmstate.global_clock

                # run i/o function
                while not isinstance(self.vmstate.current_instruction, ReturnOperation):
                    self.vmstate.run_step()

                # return from i/o function
                self.vmstate.run_step()

                function_name = current_instruction.name.replace(self.vmstate.ir_function_prefix, '')

                io_name = OutputSkeleton.output_names[function_name]
                io_value = OutputManager.output_table[io_name]

                if io_name not in out_vals:
                    out_vals[io_name] = io_value
                else:
                    idempotency = OutputManager.IDEMPOTENT if io_value == out_vals[io_name] else OutputManager.NON_IDEMPOTENT
                    required_idempotency = OutputManager.output_idempotency_table[io_name]
                    OutputManager.measure_idempotency(io_name, idempotency)

                    if idempotency != required_idempotency:
                        anomaly = OutputAnomaly(checkpoint_pc, checkpoint_clock, self.vmstate.register_file.pc, self.vmstate.global_clock, io_name, idempotency, required_idempotency)
                        if anomaly not in self.vmstate.anomalies:
                            self.vmstate.anomalies.append(anomaly)


                # create tracking information
                runinfo = RunInfo('OUTPUT', pc, global_clock, reset_no[resetting_out], function_name, io_name, io_value)

                # append tracking information
                tracking[resetting_out].append(runinfo)

                reset_no[resetting_out] += 1
                
                if reset_no[resetting_out] == 1:
                    self.vmstate.reset()
                    self.checkpoint_manager.do_restore()

                else:
                    self.checkpoint_manager.restore_dump()

            # run the operation. If an exception occurs, sign it and skip tracking (cannot continue)
            try:
                self.vmstate.run_step()

            except MemoryException as e:
                self.ignore_pc.append(checkpoint_pc)
                tracking[resetting_out].append('Unable to continue the analysis due to a MemoryException: {}'.format(e))
                self.checkpoint_manager.restore_dump()
                force_stop = True
                break

        # append to global tracking info
        self.vmstate.profiling[checkpoint_clock] = tracking

        if force_stop:
            raise StopException()
