import numpy as np

from collections import defaultdict

from ScEpTIC.AST.elements.instructions.other_operations import CallOperation
from ScEpTIC.emulator.intermittent_executor.anomalies import LinearAnomaly

from .base import InterruptionManager


class LocateMemoryAnomaliesInterruptionManager(InterruptionManager):
    """
    Interruption manager for locating memory-related intermittence anomalies
    """
    collect_memory_trace = True
    
    def __init__(self, vmstate, checkpoint_manager):
        super().__init__(vmstate, checkpoint_manager)
        
        if checkpoint_manager.stop_on_power_interrupt:
            self.vmstate.execution_depth = 0

        # if checkpoint placement is dynamic, checkpoints are taken when an interrupt happens.
        self.is_dynamic = self.checkpoint_manager.checkpoint_placement == 'dynamic'


    def _append_anomaly_to_anomalies(self, anomaly):
        """
        Append anomaly to anomalies list. If the anomaly was saved as false-positive, set it as actual anomaly
        """

        # anomaly infos
        anomaly_name = anomaly.anomaly_name
        consumer_pc = anomaly.consumer_op.pc_tree
        producer_pc = anomaly.producer_op.pc_tree
        element = anomaly.element

        # If target cell not present -> insert it.
        if element not in self.vmstate.anomalies[anomaly_name][consumer_pc][producer_pc]:
            self.vmstate.anomalies[anomaly_name][consumer_pc][producer_pc][element] = anomaly

        # Otherwise, update false positive information
        else:
            self.vmstate.anomalies[anomaly_name][consumer_pc][producer_pc][element].false_positive &= anomaly.false_positive


    def _manage_anomalies_dict(self):
        """
        Transform the data structure into a list of actual anomalies
        """

        anomalies_list = []

        anomalies_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for anomaly_name in self.vmstate.anomalies:
            anomalies = self.vmstate.anomalies[anomaly_name]

            # CONSUMER PC
            for consumer_pc in anomalies:

                # PRODUCER PC
                for producer_pc in anomalies[consumer_pc]:
                    # Aggregate elements (anomalous memory cells) into a single anomaly

                    anomaly_list = anomalies[consumer_pc][producer_pc]
                    anomaly_list = list(anomaly_list.values())

                    anomaly = anomaly_list[0]
                    anomaly._init_lists()

                    for anomalous_element in anomaly_list[1:]:
                        anomaly.add_element(anomalous_element)

                    lv1_consumer_pc = anomaly.get_consumer_pc()
                    lv1_producer_pc = anomaly.get_producer_pc()
                    n_elements = len(anomaly.elements)

                    for b in anomalies_dict[lv1_consumer_pc][lv1_producer_pc][n_elements]:
                        if anomaly.elements == b.elements:
                            b.add_other_pc(anomaly)
                            break

                    # "NoBreak"
                    else:
                        anomalies_dict[lv1_consumer_pc][lv1_producer_pc][n_elements].append(anomaly)
        
        for pc1 in anomalies_dict.values():
            for pc2 in pc1.values():
                for anomaly_list in pc2.values():
                    for anomaly in anomaly_list:
                        # include anomaly into anomalies list
                        anomalies_list.append(anomaly)

        self.vmstate.anomalies = anomalies_list

        # stats
        self.vmstate.stats.anomaly_found(len(self.vmstate.anomalies))

    def _analyze_memory_trace(self, memory_trace, consumer, producer):
        """
        Scans the consumer and producer traces to find write-after-read dependencies
        Parameters:
            memory_trace: the memory trace dictionary
            consumer: the name of the consumer key of the memory_trace
            producer: the name of the producer key of the memory_trace
        """

        # generate list of consumers clocks
        consumers = np.array([consumer_clock for consumer_clock in memory_trace[consumer].keys()])

        do_first_consumer_check = True

        # for each producer operation (orderedDict), verify the consumer it influences
        for producer_clock in memory_trace[producer]:

            # get producer operation
            producer_op = memory_trace[producer][producer_clock]

            # If dynamic analysis -> analyze only the previous #ED operations with respect to the producer's clock
            if self.is_dynamic:
                # binary search of "producer_clock - ED"
                index = np.searchsorted(consumers, producer_clock - self.vmstate.execution_depth)
                # Remove unreachable consumers
                consumers = consumers[index:]

            # If static checkpoints -> remove all consumer clock after first producer
            elif do_first_consumer_check:
                # binary search of producer_clock
                index = np.searchsorted(consumers, producer_clock)

                # Remove consumers that pass the first producer
                # NB: CHK -> STORE -> LOAD -> STORE ...
                # The LOAD will never access an anomalous value, since the first STORE keep the value consistent
                # CHK -> LOAD -> STORE -> LOAD -> STORE
                # This also happens for the second LOAD, which can never access the value produced by the second STORE
                # in a static checkpoint scenario
                consumers = consumers[:index]

                # We must perform the above operations only with the first producer
                # so we disable further checks
                do_first_consumer_check = False

            # for each consumer operation that access the value produced by the producer operation
            for consumer_clock in consumers:

                # if the consumer is a future operation, analysis on current producer ends
                if consumer_clock > producer_clock:
                    break

                # get consumer operation
                consumer_op = memory_trace[consumer][consumer_clock]

                # If something changes -> actual anomaly. Otherwise -> false positive
                is_false_positive = consumer_op.value == producer_op.value and consumer_op.dimension == producer_op.dimension and consumer_op.address == producer_op.address

                # Create anomaly and track it
                anomaly = LinearAnomaly(consumer_op, producer_op, consumer, producer, is_false_positive)
                self._append_anomaly_to_anomalies(anomaly)


    def _analyze_memory_trace_heap(self, memory_trace):
        """
        Performs the calls to self._analyze_memory_trace() for analyzing Memory Map Anomalies
        """

        # LOAD -> FREE
        self._analyze_memory_trace(memory_trace, 'read', 'deallocation')

        # LOAD -> FREE -> MALLOC / LOAD -> REALLOC
        self._analyze_memory_trace(memory_trace, 'read', 'allocation')

        # STORE -> FREE
        self._analyze_memory_trace(memory_trace, 'write', 'deallocation')

        # STORE -> FREE -> MALLOC / STORE -> REALLOC
        self._analyze_memory_trace(memory_trace, 'write', 'allocation')

        # FREE -> FREE / FREE -> REALLOC / REALLOC -> REALLOC
        self._analyze_memory_trace(memory_trace, 'deallocation', 'deallocation')
        
        # REALLOC -> MALLOC / REALLOC -> REALLOC
        self._analyze_memory_trace(memory_trace, 'deallocation', 'allocation')
        
        # REALLOC -> REALLOC
        self._analyze_memory_trace(memory_trace, 'allocation', 'allocation')


    def analyze_memory_traces(self):
        """
        Analyzes memory traces
        """

        for memory_trace in self.vmstate.memory_trace.values():

            # Analyze READ -> WRITE dependencies (Data Access Anomaly and Activation Record Anomaly)
            self._analyze_memory_trace(memory_trace, 'read', 'write')

            # Analyze Memory Map Anomaly
            self._analyze_memory_trace_heap(memory_trace)

    def intermittent_execution_required(self):
        """
        The analysis runs inside run_with_intermittent_execution
        """

        return True


    def run_with_intermittent_execution(self):
        """
        Runs the test
        """

        self.vmstate.anomalies = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

        while not self.vmstate.program_end_reached:
            # If static checkpoint mechanism
            if not self.is_dynamic:
    
                # Get current instruction
                current_instruction = self.vmstate.current_instruction

                # If current instruction is a checkpoint -> analysis window end reached
                if isinstance(current_instruction, CallOperation) and current_instruction.name == self.checkpoint_manager.routine_names['checkpoint']:

                    # Analyze memory traces
                    self.analyze_memory_traces()

                    # Empty memory traces
                    self.vmstate.memory_trace = {}

                    # skip checkpoint
                    self.vmstate.register_file.pc.increment_pc()
                    self.vmstate.global_clock += 1

            # Run operation
            self.vmstate.run_step()

        # Analyze remaining memory traces
        self.analyze_memory_traces()

        # Generate anomalies
        self._manage_anomalies_dict()
