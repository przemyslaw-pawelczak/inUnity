import copy
import logging

from ScEpTIC.AST.builtins.builtin import Builtin
from ScEpTIC.exceptions import ConfigurationException


class InputManager:
    """
    This class permits to create and manage all the inputs.
    To create a standard input (one with no arguments which just a simple value attachable to it), just use the create_input method.
    To create a complex input:
        1) Extend class InputSkeleton (re-implementing the get_val() method, to suit your needs)
        2) Call the define_input() method on the extended class with the appropriate parameters
    """
    
    # constants
    LONG_TERM = 'LONG_TERM'
    MOST_RECENT = 'MOST_RECENT'

    inputs = {}
    consistency_models = {}
    input_table = {}

    @classmethod
    def create_input(cls, input_name, function_name, return_type):
        """
        Creates a standard input.
        Name is the identifier considered by the input manager, function_name is the one appearing in the code.
        """

        logging.info('Creating input "{}" on function {}.'.format(input_name, function_name))

        if input_name in cls.inputs:
            raise ConfigurationException('An input named {} is already defined!'.format(input_name))

        input_class = type(input_name, (InputSkeleton,), {})
        input_class._create_input(input_name, function_name, '', return_type)
        cls.inputs[input_name] = input_class


    @classmethod
    def _add_custom_input(cls, input_name, input_class):
        """
        Add a custom input to the one managed by the InputManager
        """
        logging.info('Adding custom input "{}" to the input list.'.format(input_name))

        if input_name in cls.inputs:
            raise ConfigurationException('An input named {} is already defined!'.format(input_name))

        cls.inputs[input_name] = input_class

    @classmethod
    def set_input_value(cls, input_name, value):
        """
        Sets an input value to the given one.
        """
        logging.info('Setting input "{}" value to {}.'.format(input_name, value))

        if input_name not in cls.inputs:
            raise ConfigurationException('Input named {} not found!'.format(input_name))

        input_class = cls.inputs[input_name]
        input_class.value = copy.deepcopy(value)

    @classmethod
    def get_input_value(cls, input_name):
        """
        Gets the value of a given input
        """

        logging.info('Getting input "{}" value.'.format(input_name))

        if input_name not in cls.inputs:
            raise ConfigurationException('Input named {} not found!'.format(input_name))

        input_class = cls.inputs[input_name]
        return input_class.value


    @classmethod
    def set_consistency_model(cls, input_name, consistency_model):
        """
        Sets an input consistency model.
        """

        cls._validate_consistency_model(consistency_model)

        if input_name not in cls.inputs:
            raise ConfigurationException('Input named {} not found!'.format(input_name))

        cls.consistency_models[input_name] = consistency_model


    @classmethod
    def get_consistency_model(cls, input_name):
        """
        Returns the consistency model of a given input.
        """

        if input_name not in cls.consistency_models:
            return None

        return cls.consistency_models[input_name]
        

    @classmethod
    def _validate_consistency_model(cls, consistency_model):
        """
        Validates a consistency model.
        """

        if consistency_model not in [cls.LONG_TERM, cls.MOST_RECENT]:
            raise ConfigurationException('Invalid consistency model {}.'.format(consistency_model))


class InputSkeleton(Builtin):
    """
    Skeleton of an user-defined input.
    """

    # input configurations
    input_name = None
    value = None

    # input tracking information
    input_functions = {}
    input_names = {}

    # recognizer for builtin linker
    is_input = True

    def get_val(self):
        """
        Returns the value of the input when the input operation is run.
        """

        # Allows a cyclic list as input value
        # [1,2,3] -> first time return 1, then 2, then 3, then 1, and so on
        if isinstance(self.value, list):
            value = self.value.pop(0)
            self.value.append(value)

        else:
            value = self.value

        InputManager.input_table[self.input_name] = value
        return value

    @classmethod
    def _create_input(cls, input_name, function_name, arguments, return_type):
        """
        Creates an input builtin. This method can be called only by InputManager.
        To define more complex inputs, extend this class and then use the define_input method to link it to the AST.
        The input name is the identifier of the input, the other arguments are the same of the Builtin class.
        """
    
        # Input class already defined
        if cls.input_name is not None:
            raise ConfigurationException('Input class already defined on name "{}" with function {}().'.format(cls.input_name, cls.input_functions[cls.input_name]))
        
        # Input name defined
        if input_name in cls.input_functions.keys():
            raise ConfigurationException('Unable to define input name "{}" on function {}().\nInput name "{}" is already defined with function {}().'.format(input_name, function_name, input_name, cls.input_functions[input_name]))

        # Input function defined
        if function_name in cls.input_names.keys():
            raise ConfigurationException('Unable to define input function {}() on name "{}".\nInput function {}() is already defined on name "{}".'.format(function_name, input_name, function_name, cls.input_names[function_name]))

        cls.input_name = input_name
        cls.input_names[function_name] = input_name
        cls.input_functions[input_name] = function_name
        cls.define_builtin(function_name, arguments, return_type)

    @classmethod
    def define_input(cls, input_name, function_name, arguments, return_type):
        """
        Defines a custom input builtin.
        input_name is the identifier of the input considered by the input manager.
        The other arguments are the same of the Builtin class.
        """

        cls._create_input(input_name, function_name, arguments, return_type)
        InputManager._add_custom_input(input_name, cls)
