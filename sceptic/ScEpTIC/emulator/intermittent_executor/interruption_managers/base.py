from ScEpTIC.emulator.intermittent_executor.anomalies import SingleStackARAnomaly, StackARAnomaly
from ScEpTIC.exceptions import ConfigurationException


class InterruptionManager:
    """
    Base interruption manager
    """

    do_data_anomaly_check = False
    input_lookup_enabled = False
    requires_static_checkpoint = False
    collect_memory_trace = False

    def __init__(self, vmstate, checkpoint_manager):
        self.vmstate = vmstate
        self.checkpoint_manager = checkpoint_manager


    def _stack_check_at_address(self, address, element_name):
        """
        Verifies if at a given address there is a stack anomaly.
        """

        expected_value = self.checkpoint_manager.dump['stack']._memory[address]

        anomalous = False
        anomaly = None

        try:
            real_value = self.vmstate.memory.stack._memory[address]
            
            # value differs
            if expected_value.content != real_value.content or expected_value.dimension != real_value.dimension:
                anomaly   = SingleStackARAnomaly(expected_value, real_value, element_name, False)
                anomalous = True
            
            # element modified with the same value
            elif real_value.lookup['write_global_clock'] > self.vmstate.global_clock or real_value.lookup['memory_mapped'] > self.vmstate.global_clock or real_value.lookup != expected_value.lookup:
                anomaly = SingleStackARAnomaly(expected_value, real_value, element_name, True)

        # element not present anymore (memory re-mapped)
        except KeyError:
            anomaly   = SingleStackARAnomaly(expected_value, None, element_name, True)
            anomalous = True

        return anomalous, anomaly


    def has_stack_activation_record_anomalies(self, reset_pc, append_anomaly = True):
        """
        Verifies if the stack portion of a call is modified by subsequent operations.
        """

        anomalous_grp = False
        anomalies = []
        
        checkpoint_pc = self.checkpoint_manager.checkpoint['register_file'].pc
        
        # checks saved regs
        for address in self.checkpoint_manager.dump['function_call_lookup']['regs']:
            anomalous, anomaly = self._stack_check_at_address(address, 'Register')
            
            anomalous_grp |= anomalous

            InterruptionManager._append_anomaly(anomalies, anomaly)

        # checks for passed arguments
        for address in self.checkpoint_manager.dump['function_call_lookup']['args']:
            anomalous, anomaly = self._stack_check_at_address(address, 'Argument')
            
            anomalous_grp |= anomalous

            InterruptionManager._append_anomaly(anomalies, anomaly)

        # checks for saved pc
        if self.checkpoint_manager.dump['function_call_lookup']['pc'] is not None:
            pc_address = self.checkpoint_manager.dump['function_call_lookup']['pc']
            anomalous, anomaly = self._stack_check_at_address(pc_address, 'PC')
            
            anomalous_grp |= anomalous
            
            InterruptionManager._append_anomaly(anomalies, anomaly)

        # checks for saved ebp
        if self.checkpoint_manager.dump['function_call_lookup']['ebp'] is not None:
            ebp_address = self.checkpoint_manager.dump['function_call_lookup']['ebp']
            anomalous, anomaly = self._stack_check_at_address(ebp_address, 'EBP')
            
            anomalous_grp |= anomalous

            InterruptionManager._append_anomaly(anomalies, anomaly)

        if append_anomaly and anomalous_grp:
            anomaly = StackARAnomaly(anomalies, checkpoint_pc, self.checkpoint_manager.checkpoint['global_clock'], reset_pc)

            if anomaly not in self.vmstate.anomalies:
                self.vmstate.anomalies.append(anomaly)

                # stats
                self.vmstate.stats.anomaly_found()
            
        # If stop on first anomaly found
        if anomalous_grp:
            self.vmstate.handle_stop_request(anomaly)

        return anomalous_grp


    def intermittent_execution_required(self):
        """
        Returns if the current operation requires an intermittent execution.
        Retruns always false, as base simulates a continuous execution
        """

        return False


    def run_with_intermittent_execution(self):
        """
        Runs tests in intermittent execution scenario.
        """

        raise ConfigurationException('Not implemented. Please implement this method in your InterruptionManager extension!')


    @staticmethod
    def _append_anomaly(anomalies, anomaly):
        
        if anomaly is not None:
            anomalies.append(anomaly)
