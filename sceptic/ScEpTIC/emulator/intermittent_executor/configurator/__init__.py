import logging
import os

from ScEpTIC.exceptions import ConfigurationException

def load_prebuilt_config(config):
    """
    Loads a pre-built configuration, given the name specified in the configuration file.
    In order to add other configurations, just create a .py file named with the name of your configuration.
    """

    # check if config.system is present and of correct type
    if 'system' not in config.__dict__:
        raise ConfigurationException('System type not specified in configuration file!')

    elif not isinstance(config.system, str):
        raise ConfigurationException('System type must be a string, {} given.'.format(config.system.__class__.__name__))

    logging.info('Loading configuration for {}.'.format(config.system))

    # if system is custom, no loading is required.
    if config.system == 'custom':
        return

    # if config file not present in ScEpTIC/emulator/configurator/ raise an exception.
    if config.system+'.py' not in os.listdir(os.path.dirname(__file__)):
        raise ConfigurationException('Pre-built config for {} not found.'.format(config.system))

    # import the configuration
    prebuilt_config = __import__(__name__+'.'+config.system, fromlist=['memory_configuration', 'checkpoint_mechanism_configuration'])
    
    # get the configurations to be set
    memory_configuration = prebuilt_config.memory_configuration
    checkpoint_mechanism_configuration = prebuilt_config.checkpoint_mechanism_configuration

    # set memory_configuration of user-provided config file
    for key in memory_configuration:
        element = memory_configuration[key]

        if isinstance(element, dict):
            for subkey in element:
                config.memory_configuration[key][subkey] = element[subkey]

        else:
            config.memory_configuration[key] = element

    # set checkpoint_mechanism_configuration of user-provided config file
    for key in checkpoint_mechanism_configuration:
        element = checkpoint_mechanism_configuration[key]

        if isinstance(element, dict):
            for subkey in element:
                config.checkpoint_mechanism_configuration[key][subkey] = element[subkey]

        else:
            config.checkpoint_mechanism_configuration[key] = element
