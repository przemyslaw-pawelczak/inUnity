import copy
import logging

from ScEpTIC.AST.builtins.builtin import Builtin
from ScEpTIC.exceptions import ConfigurationException


class OutputManager:
    """
    This class permits to create and manage all the outputs.
    To create a standard output (which uses a single argument), just use the create_output method from the OutputManager.
    To create a complex output:
        1) Extend class OutputSkeleton (re-implementing the get_val() method, to suit your needs)
        2) Call the create_output() method on the extended class with the appropriate parameters
    """

    IDEMPOTENT = 0
    NON_IDEMPOTENT = 1

    default_idempotent = False

    output_table = {}
    output_idempotency_table = {}
    measured_idempotency = {}

    @classmethod
    def get_measured_idempotency(cls):
        """
        Returns a visual representation of the measured idempotency
        """
        measured = {}
        for name, val in cls.measured_idempotency.items():
            measured[name] = 'IDEMPOTENT' if val == cls.IDEMPOTENT else 'NON-IDEMPOTENT'

        return measured


    @classmethod
    def measure_idempotency(cls, output_name, idempotency):
        """
        Sets the measured idempotency for the given output
        """
        val = cls.measured_idempotency[output_name]
        
        if val == None or val == cls.IDEMPOTENT:
            cls.measured_idempotency[output_name] = idempotency

    @classmethod
    def set_default_idempotent(cls, default_idempotent):
        """
        Set the default idempotency for all outputs
        """
        cls.default_idempotent = default_idempotent

    @classmethod
    def create_output(cls, output_name, function_name, arguments):
        """
        Creates a standard output.
        Name is the identifier considered by the output manager, function_name is the one appearing in the code.
        """

        logging.info('Creating output "{}" on function {}.'.format(output_name, function_name))

        if output_name in cls.output_table:
            raise ConfigurationException('An output named {} is already defined!'.format(output_name))

        output_class = type(output_name, (OutputSkeleton,), {})
        output_class.define_output(output_name, function_name, arguments, 'void')


    @classmethod
    def reset(cls):
        """
        Resets all the output values.
        """
        for key in cls.output_table:
            cls.output_table[key] = None


    @classmethod
    def get_changes(cls):
        """
        Returns all the outputs with non-null value, which are the ones that are set on current program run.
        """

        changed = {}

        for output, output_val in cls.output_table.items():

            if output_val is not None:
                changed[output] = copy.deepcopy(output_val)

        return changed

    @classmethod
    def set_idempotency(cls, name, idempotency):
        """
        Sets the idempotency model of a given output.
        """

        if name not in cls.output_idempotency_table:
            raise ConfigurationException('No output named {} is defined.'.format(name))

        if idempotency != cls.IDEMPOTENT and idempotency != cls.NON_IDEMPOTENT:
            raise ConfigurationException('Invalid idempotency model for {}.'.format(name))

        cls.output_idempotency_table[name] = idempotency

    @classmethod
    def dump(cls):
        """
        Dumpts the output table
        """
        return copy.deepcopy(cls.output_table)

    @classmethod
    def restore(cls, output_table):
        """
        Restores the output table
        """
        cls.output_table = copy.deepcopy(output_table)

    @classmethod
    def diff(cls, output_table):
        """
        Diffs the current output table with a dump
        """
        diffs = []

        for name, current_val in cls.output_table.items():
            dump_val = output_table[name]

            if current_val != dump_val:
                diff.append({'output': name, 'dump_value': copy.deepcopy(dump_val), 'current_value': copy.deepcopy(current_val)})

        return duffs


class OutputSkeleton(Builtin):
    """
    Skeleton of an user-defined output.
    """

    # output configuration
    output_name = None

    # output tracking information
    output_functions = {}
    output_names = {}

    def __init__(self):
        self.output_init()
        super().__init__()

    def get_val(self):
        """
        Sets the value of the output when the output operation is run.
        Note that this method is named "get_val" as the OutputSkeleton extends the Instruction base class.
        """

        value = self.args
        self.set_output_val(value)
        return None

    def output_init(self):
        return None

    def get_output_val(self):
        """
        Returns the output value (i.e. environment state)
        """
        return OutputManager.output_table[self.output_name]


    def set_output_val(self, value):
        """
        Updates the output value (that is, the environment state)
        """
        OutputManager.output_table[self.output_name] = value


    @classmethod
    def define_output(cls, output_name, function_name, arguments, return_type):
        """
        Creates an output builtin.
        To define a simple output, just call the create_output method from the OutputManager class.
        To define more complex outputs, extend this class and then use this method to link it to the AST.
        The output_name is the identifier of the output, the other arguments are the same of the Builtin class.
        """

        # Output class already defined
        if cls.output_name is not None:
            raise ConfigurationException('Output class already defined on name "{}" with function {}().'.format(cls.output_name, cls.output_functions[cls.output_name]))
        
        # Output name defined
        if output_name in cls.output_functions.keys():
            raise ConfigurationException('Unable to define output name "{}" on function {}().\nOutput name "{}" is already defined with function {}().'.format(output_name, function_name, output_name, cls.output_functions[output_name]))

        # Output function defined
        if function_name in cls.output_names.keys():
            raise ConfigurationException('Unable to define output function {}() on name "{}".\nOutput function {}() is already defined on name "{}".'.format(function_name, output_name, function_name, cls.output_names[function_name]))

        cls.output_name = output_name
        cls.output_names[function_name] = output_name
        cls.output_functions[output_name] = function_name

        OutputManager.output_table[output_name] = None

        cls.define_builtin(function_name, arguments, return_type)

        OutputManager.output_idempotency_table[output_name] = OutputManager.IDEMPOTENT if OutputManager.default_idempotent else OutputManager.NON_IDEMPOTENT
        OutputManager.measured_idempotency[output_name] = None
