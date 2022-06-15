import copy

from ScEpTIC.AST.elements.instructions.other_operations import CallOperation

from .base import InterruptionManager


class InputInterruptionManager(InterruptionManager):
    """
    Interruption manager for analyzing input policies
    """

    input_lookup_enabled = True
    requires_static_checkpoint = True

    def intermittent_execution_required(self):
        """
        To verify input anomalies no interruption is required: interruptions will only introduce war anomalies / memory map anomalies.
        Input access anomalies are measurable without running in intermittent scenario, because they refers to a previous checkpoint.
        It is sufficient to run the program sequentially: when a checkpoint is encountered, just skip it and increment the checkpoint_clock.
        The system will automatically check the input lookup table of registers and memory w.r.t. the current checkpoint_clock.
        If a discrepancy is found between the measured consistency model and the one required by the programmer, an anomaly is created.
        """
        current_instruction = self.vmstate.current_instruction

        # if checkpoint found -> increment checkpoint_clock and skip checkpoint.
        if isinstance(current_instruction, CallOperation) and current_instruction.name == self.checkpoint_manager.routine_names['checkpoint']:
            
            # increment checkpoint_clock
            self.vmstate.checkpoint_clock += 1
            
            # map checkpoint_clock to program counter
            current_clock = self.vmstate.checkpoint_clock
            self.vmstate.checkpoint_clock_pc_maps[current_clock] = copy.deepcopy(self.vmstate.register_file.pc)
            
            # skip checkpoint function
            self.vmstate.register_file.pc.increment_pc()
            self.vmstate.global_clock += 1

        return False


    def run_with_intermittent_execution(self):
        # No execution happens here
        pass
