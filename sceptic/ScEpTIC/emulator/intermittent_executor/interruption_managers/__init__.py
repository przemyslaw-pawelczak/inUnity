import logging
import os

from ScEpTIC.exceptions import ConfigurationException

def get_interruption_manager(name, class_name):
    """
    Returns the proper interruption manager class
    """

    if name+'.py' not in os.listdir(os.path.dirname(__file__)):
        raise ConfigurationException('Interruption Manager for {} not found.'.format(name))

    logging.info('[InterruptionManager] Loading Interruption Manager for {} analysis'.format(name))

    prebuilt_config = __import__(__name__+'.'+name, fromlist=[class_name])
    
    return getattr(prebuilt_config, class_name)
