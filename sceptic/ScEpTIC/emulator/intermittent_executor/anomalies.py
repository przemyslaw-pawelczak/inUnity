import copy
import logging

from ScEpTIC.emulator.io.output import OutputManager
from ScEpTIC.exceptions import AnomalyException, RuntimeException

class BaselineDataAnomaly:

    def __init__(self, cell_address, checkpoint_pc, causing_pc):
        self.cell_address = copy.deepcopy(cell_address)
        self.checkpoint_pc = copy.deepcopy(checkpoint_pc)
        self.causing_pc = copy.deepcopy(causing_pc)


    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        return (self.cell_address == '*' or other.cell_address == '*' or self.cell_address == other.cell_address) and self.checkpoint_pc == other.checkpoint_pc and self.causing_pc == other.causing_pc


    def __str__(self):
        return 'Cell address: {}\nCheckpoint happens at: {}\nCaused by: {}\n'.format(self.cell_address, self.checkpoint_pc, self.causing_pc)


class BaselineInputAnomaly:

    def __init__(self, input_name, first_checkpoint_pc, second_checkpoint_pc, required_access_model, shown_access_model):
        self.input_name = input_name
        self.first_checkpoint_pc = copy.deepcopy(first_checkpoint_pc)
        self.second_checkpoint_pc = copy.deepcopy(second_checkpoint_pc)
        self.required_access_model = required_access_model
        self.shown_access_model = shown_access_model


    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        return self.input_name == other.input_name and self.first_checkpoint_pc == other.first_checkpoint_pc and self.second_checkpoint_pc == other.second_checkpoint_pc and self.required_access_model == other.required_access_model and self.shown_access_model == other.shown_access_model


    def __str__(self):
        retval  = 'Input: {}\n'.format(self.input_name)
        retval += 'Checkpoint interval: from    {}    to    {}\n'.format(self.first_checkpoint_pc, self.second_checkpoint_pc)
        retval += 'Required access model: {}\n'.format(self.required_access_model)
        retval += 'Shown access model: {}\n'.format(self.shown_access_model)
        return retval


class DataAnomaly:
    """
    Representation of a data anomaly
    """

    def __init__(self, cell, current_pc, read_clock, is_false_positive):
        self.cell = copy.deepcopy(cell)
        self.current_pc = copy.deepcopy(current_pc)
        self.is_false_positive = is_false_positive
        self.from_memory_map = False
        self.read_clock = read_clock
        
        if self.is_false_positive:
            logging.warning('False-positive {} at {} on {}'.format(self.get_type(), self.current_pc, self.cell))


    def __str__(self):
        read_pc = self.current_pc.resolve()
        
        if isinstance(self, WARAnomaly):
            write_pc = self.cell.lookup['write_pc'].resolve()
            write_string = 'Write'
            element_name = 'value'
            clock_event = 'Written at clock: {}\n'.format(self.cell.lookup['write_global_clock'])
            description = 'Cell address: {}\nCorrect content: {}\nRead content: {}'.format(self.cell.absolute_address, self.cell.lookup['old_content'], self.cell.content)

        elif isinstance(self, MemoryMapAnomaly):
            write_pc = self.cell.lookup['memory_mapped_pc'].resolve()
            write_string = 'Mapping'
            element_name = 'address'
            clock_event = 'Mapped at clock: {}\n'.format(self.cell.lookup['memory_mapped'])
            description = 'Cell address: {}\nCell dimension: {}\nCorrect address: {}\nCorrect dimension: {}'.format(self.cell.absolute_address, self.cell.dimension, self.cell.lookup['old_memory_address'], self.cell.lookup['old_dimension'])

        false_positive = ' - False Positive ({} not modified)'.format(element_name) if self.is_false_positive else ''
        from_memory_map = ' - Value modified due to memory mapping instruction' if self.from_memory_map else ''

        read_at = 'Read at clock: {}\n'.format(self.read_clock)

        return '[{}{}{}]\n{}\n{}{}Memory Read happens at:\n{}Memory {} happens at:\n{}\n\n'.format(self.get_type(), false_positive, from_memory_map, description, read_at, clock_event, read_pc, write_string, write_pc)


    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        return self.is_false_positive == other.is_false_positive and self.current_pc == other.current_pc and self.cell.lookup['write_pc'] == other.cell.lookup['write_pc'] and self.cell.lookup['memory_mapped_pc'] == other.cell.lookup['memory_mapped_pc']


    def get_type(self):
        """
        Returns the type of the data anomaly.
        """

        return 'Data Anomaly'


    def raise_exception(self):
        """
        Raises an exception to signal the anomaly.
        """

        raise AnomalyException('{} exception at {}\n{}\n{}\n{}\n'.format(self.get_type(), self.current_pc, self.cell.__dict__, self.cell.lookup, self.read_clock))


class WARAnomaly(DataAnomaly):
    """
    Representation of a Write After Read anomaly
    """

    def get_type(self):
        return 'Write After Read Anomaly'


class MemoryMapAnomaly(DataAnomaly):
    """
    Representation of a Memory Map anomaly
    """

    def get_type(self):
        return 'Memory Map Anomaly'


class SingleStackARAnomaly:
    """
    Represents a single element of a Stack Activation Record anomaly.
    """

    def __init__(self, dump_cell, current_cell, element, is_false_positive):
        self.dump_cell = copy.deepcopy(dump_cell)
        self.current_cell = copy.deepcopy(current_cell)
        self.element = element
        self.is_false_positive = is_false_positive
    

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        return self.is_false_positive == other.is_false_positive and self.element == other.element


    def __str__(self):
        spaces = ' ' * 8
        
        if self.is_false_positive:
            false_positive = '{}(False positive: {})'.format(spaces, 'element modified with the same value' if self.current_cell is not None else 'element removed from stack')

        else:
            false_positive = ''

        if self.current_cell is not None:
            current_dim  = '{} bytes'.format(self.current_cell.dimension)
            current_content = self.current_cell.content
            written_clock = self.current_cell.lookup['write_global_clock']

        else:
            current_dim  = None
            current_content = None
            written_clock = None

        write_clock = '{}Written at clock: {}\n'.format(spaces, written_clock)
        current_dim = '{}Current dimension: {}\n'.format(spaces, current_dim)
        dump_dim = '{}Expected dimension: {} bytes\n'.format(spaces, self.dump_cell.dimension)
        current_content = '{}Current content: {}\n'.format(spaces, current_content)
        dump_content = '{}Expected content: {}\n'.format(spaces, self.dump_cell.content)

        return '[{}] {}:{}\n{}{}{}{}{}\n'.format(self.dump_cell.absolute_address, self.element, false_positive, write_clock, current_dim, dump_dim, current_content, dump_content)
        

"""
Represents a Stack Activation Record Anomaly (which will contain a SingleStackARAnomaly for each anomalous stack element).
"""
class StackARAnomaly:

    def __init__(self, anomalies, checkpoint_pc, checkpoint_clock, reset_pc):
        self.anomalies = copy.deepcopy(anomalies)
        self.checkpoint_pc = copy.deepcopy(checkpoint_pc)
        self.checkpoint_clock = checkpoint_clock
        self.reset_pc = copy.deepcopy(reset_pc)


    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        return self.anomalies == other.anomalies and self.reset_pc == other.reset_pc and self.checkpoint_pc == other.checkpoint_pc


    def get_type(self):
        return 'Stack Activation Record Anomaly'


    def __str__(self):
        checkpoint_pc = self.checkpoint_pc.resolve()
        reset_pc = self.reset_pc.resolve()

        anomalies = ''

        for anomaly in self.anomalies:
            anomalies += '{}{}'.format(' '*4, anomaly)

        return '[{}]\nAnalysis of following checkpoint cannot be completed:\n{}Resets operation happens at:\n{}Stack used at clock: {}\nFound anomalies:\n{}\n'.format(self.get_type(), checkpoint_pc, reset_pc, self.checkpoint_clock, anomalies)


"""
Represents a Memory Access Anomaly (which will cause a MemoryException and in real scenario might cause the MCU to stop the execution)
"""
class MemoryAccessAnomaly:

    def __init__(self, generating_pc, generating_clock, current_pc, current_clock, checkpoint_pc, message):
        self.generating_pc = copy.deepcopy(generating_pc)
        self.generating_clock = generating_clock
        self.current_pc = copy.deepcopy(current_pc)
        self.current_clock = current_clock
        self.checkpoint_pc = copy.deepcopy(checkpoint_pc)

        # adjust for checkpoint done
        self.checkpoint_pc.instruction_number -= 1

        self.message = message


    def get_type(self):
        return 'Memory Access Anomaly'


    def __str__(self):
        reset_pc = self.generating_pc.resolve()
        current_pc = self.current_pc.resolve()
        checkpoint_pc = self.checkpoint_pc.resolve()

        memory_access = 'Memory Access at clock: {}\n'.format(self.current_clock)
        reset_op = 'Reset happens at clock: {}\n'.format(self.generating_clock)

        return '[{}]\nException message: {}\nAnalysis of following checkpoint cannot be completed:\n{}{}{}Reset operation happens at:\n{}MemoryException happens at:\n{}\n'.format(self.get_type(), self.message, checkpoint_pc, memory_access, reset_op, reset_pc, current_pc)


    def __eq__(self, other):
        if not isinstance(other, MemoryAccessAnomaly):
            return False

        return self.generating_pc == other.generating_pc and self.current_pc == other.current_pc

class OutputAnomaly:
    """
    Represents an output anomaly
    """

    def __init__(self, checkpoint_pc, access_clock, access_pc, checkpoint_clock, output_name, measured_consistency_model, imposed_consistency_model):
        self.checkpoint_pc = copy.deepcopy(checkpoint_pc)
        self.checkpoint_clock = checkpoint_clock
        self.access_pc = copy.deepcopy(access_pc)
        self.access_clock = access_clock
        self.output_name = output_name
        self.measured_consistency_model = measured_consistency_model
        self.imposed_consistency_model = imposed_consistency_model


    def get_type(self):
        return 'Output Access Anomaly'

    def _format_consistency(self, data):
        return 'IDEMPOTENT' if data == OutputManager.IDEMPOTENT else 'NON-IDEMPOTENT'

    def __str__(self):
        output_name = 'output name: {}\n'.format(self.output_name)
        required_consistency = 'Required consistency model: {}\n'.format(self._format_consistency(self.imposed_consistency_model))
        measured_consistency = 'Measured consistency model: {}\n'.format(self._format_consistency(self.measured_consistency_model))
        checkpoint_clock = 'Output saved at checkpoint #{}\n'.format(self.checkpoint_clock)
        access_clock = 'Output accessed at checkpoint #{}\n'.format(self.access_clock)
        checkpoint_pc = 'Checkpoint happens at:\n{}'.format(self.checkpoint_pc.resolve())
        access_pc = 'Output Access happens at:\n{}'.format(self.access_pc.resolve())
        
        return '[{}]\n{}{}{}{}{}{}{}'.format(self.get_type(), output_name, required_consistency, measured_consistency, checkpoint_clock, access_clock, checkpoint_pc, access_pc)
    

    def __eq__(self, other):
        if not isinstance(other, OutputAnomaly):
            return False

        return self.checkpoint_pc == other.checkpoint_pc and self.access_pc == other.access_pc and self.output_name == other.output_name and self.measured_consistency_model == other.measured_consistency_model

class InputPolicyAnomaly:
    """
    Represents an Input Policy Anomaly
    """

    def __init__(self, checkpoint_pc, access_clock, access_pc, checkpoint_clock, input_name, measured_consistency_model, imposed_consistency_model):
        self.checkpoint_pc = copy.deepcopy(checkpoint_pc)
        self.checkpoint_clock = checkpoint_clock
        self.access_pc = copy.deepcopy(access_pc)
        self.access_clock = access_clock
        self.input_name = input_name
        self.measured_consistency_model = measured_consistency_model
        self.imposed_consistency_model = imposed_consistency_model


    def get_type(self):
        return 'Input Access Anomaly'


    def __str__(self):
        input_name = 'Input name: {}\n'.format(self.input_name)
        required_consistency = 'Required consistency model: {}\n'.format(self.imposed_consistency_model)
        measured_consistency = 'Measured consistency model: {}\n'.format(self.measured_consistency_model)
        checkpoint_clock = 'Input saved at checkpoint #{}\n'.format(self.checkpoint_clock)
        access_clock = 'Input accessed at checkpoint #{}\n'.format(self.access_clock)
        checkpoint_pc = 'Checkpoint happens at:\n{}'.format(self.checkpoint_pc.resolve())
        access_pc = 'Input Access happens at:\n{}'.format(self.access_pc.resolve())
        
        return '[{}]\n{}{}{}{}{}{}{}'.format(self.get_type(), input_name, required_consistency, measured_consistency, checkpoint_clock, access_clock, checkpoint_pc, access_pc)
    

    def __eq__(self, other):
        if not isinstance(other, InputPolicyAnomaly):
            return False

        return self.checkpoint_pc == other.checkpoint_pc and self.access_pc == other.access_pc and self.input_name == other.input_name and self.measured_consistency_model == other.measured_consistency_model


class LinearAnomaly:
    """
    Represents a Base anomaly for the DataLinearInterruptionManager
    """

    heap_memory_traces = ['allocation', 'deallocation']

    def __init__(self, consumer_op, producer_op, consumer, producer, false_positive):
        self.consumer_op = consumer_op
        self.consumer = consumer
        self.producer_op = producer_op
        self.producer = producer
        self.false_positive = false_positive
        self.element = ''

        if consumer in self.heap_memory_traces or producer in self.heap_memory_traces:
            self.anomaly_name = 'Memory Map Anomaly'

            # If metadata available -> use it
            if self.consumer_op.metadata is None:
                self.element = 'Memory address {}'.format(self.consumer_op.address)

            else:
                self.element = self.consumer_op.metadata

        # If consumer and producer happen in different functions -> it may be an activation record anomaly
        elif self.consumer_op.pc.function_name != self.producer_op.pc.function_name:
            self.anomaly_name = 'Activation Record Anomaly'
            
            # If metadata available -> Global var or local element
            if self.consumer_op.metadata is not None:

                # If the producer alters a global variable -> Data Access Anomaly
                if 'Global variable ' in self.consumer_op.metadata:
                    self.anomaly_name = 'Data Access Anomaly'
                    self.element = self.consumer_op.metadata

                # Otherwise, it is an Activation Record Anomaly
                else:
                    self.element = '{} of function {}'.format(self.consumer_op.metadata, self.consumer_op.pc.function_name)

            # If no metadata present -> Activation Record Anomaly
            else:
                self.element = 'Memory address {}'.format(self.consumer_op.address)
        
        # Otherwise it is a Data Access Anomaly
        else:
            self.anomaly_name = 'Data Access Anomaly'
            
            if self.consumer_op.metadata is not None:

                if 'Global variable' in self.consumer_op.metadata:
                    self.element = self.consumer_op.metadata

                else:
                    self.element = '{} of function {}'.format(self.consumer_op.metadata, self.consumer_op.pc.function_name)

            else:
                self.element = 'Memory address {}'.format(self.consumer_op.address)


    def get_debug_data_element(self):
        return {
            'read_value': self.consumer_op.value,
            'read_clock': self.consumer_op.clock,
            'write_value': self.producer_op.value,
            'write_clock': self.producer_op.clock
        }


    def _init_lists(self):
        # list of elements with the same anomaly
        self.elements = [self.element]
        
        # list of false-positivity of such elements
        self.elements_fp = [self.false_positive]
        
        # list of anomaly descriptions of such elements (e.g. read->write)
        self.elements_cp = ['{} -> {}'.format(self.consumer, self.producer)]

        # list of debug data for the element
        self.elements_db = [self.get_debug_data_element()]
        self.other_pc = set()


    def add_element(self, anomaly):
        """
        Add an element to the anomaly element list
        """

        element = anomaly.element
        false_positive = anomaly.false_positive

        # if at least one element is not false positive, the anomaly is real
        self.false_positive = self.false_positive and false_positive

        if element in self.elements:
            index = self.elements.index(element)
            self.elements_fp[index] = self.elements_fp[index] and false_positive

        else:
            self.elements.append(element)
            self.elements_fp.append(false_positive)
            self.elements_cp.append('{} -> {}'.format(self.consumer, self.producer))
            self.elements_db.append(anomaly.get_debug_data_element())


    def add_other_pc(self, other_anomaly):
        """
        Add another call path that causes the same anomaly
        """

        if len(self.other_pc) > 5:
            return
            
        consumer_pc = '{}'.format(other_anomaly.consumer_op.pc.resolve())
        producer_pc = '{}'.format(other_anomaly.producer_op.pc.resolve())
        other = (consumer_pc, producer_pc)
        self.other_pc.add(other)


    def get_element(self):
        """
        Return the only element of the newly found anomaly
        """

        if len(self.elements) > 1:
            raise RuntimeException('More than one element in the anomaly!')

        return self.elements[0], self.elements_fp[0]


    def get_consumer_pc(self):
        """
        Returns a textual representation of the consumer program counter
        """

        return '{}'.format(self.consumer_op.pc)


    def get_producer_pc(self):
        """
        Returns a textual representation of the producer program counter
        """

        return '{}'.format(self.producer_op.pc)


    def _repr_pc(self, consumer_pc, producer_pc, spacer):
        # Heap re-execution
        if consumer_pc == producer_pc:
            retstr = '{}Memory access and alteration happens at: {}\n\n'.format(spacer, consumer_pc)
        
        else:
            retstr = '{}Memory access happens at: {}\n'.format(spacer, consumer_pc)
            retstr = '{}{}Memory alteration happens at: {}\n\n'.format(retstr, spacer, producer_pc)

        return retstr


    def __str__(self):
        spacer = ' '*4

        retstr = '[{}{}]\n'.format(self.anomaly_name, ' - False Positive' if self.false_positive else '')
        retstr = '{}{}'.format(retstr, self._repr_pc(self.consumer_op.pc.resolve(), self.producer_op.pc.resolve(), spacer))

        for consumer_pc, producer_pc in self.other_pc:
            retstr = '{}{}Also:\n\n\n{}'.format(retstr, spacer, self._repr_pc(consumer_pc, producer_pc, spacer))

        retstr = '{}{}{}:\n'.format(retstr, spacer, 'Element' if len(self.elements) == 1 else 'Elements')

        for element, false_positive, cons_prod, debug_data in zip(self.elements, self.elements_fp, self.elements_cp, self.elements_db):
            retstr = '{}{}{}{} [{}]\n'.format(retstr, spacer*2, element, ' (FALSE POSITIVE)' if false_positive else '', cons_prod)
        
            for k, v in sorted(debug_data.items(), key=lambda x: "0"+x[0] if x[0].endswith('_clock') else x[0]):
                retstr = '{}{}{}: {}\n'.format(retstr, spacer*3, k, v)
        
            retstr = '{}\n'.format(retstr)

        return '{}\n\n'.format(retstr)


    def __eq__(self, other):
        """
        Two anomalies are equal if they have the same program counters (write, read) and they have the same anomaly type
        """

        return self.anomaly_name == other.anomaly_name and self.consumer_op.pc_tree == other.consumer_op.pc_tree and self.producer_op.pc_tree == other.producer_op.pc_tree
