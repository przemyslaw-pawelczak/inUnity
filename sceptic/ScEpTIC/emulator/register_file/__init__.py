from ScEpTIC.exceptions import ConfigurationException

from .physical_register_file import PhysicalRegisterFile
from .virtual_register_file import VirtualRegisterFile

def validate_configuration(register_file_configuration):
    """
    Validates the register file configuration passed by the user.
    On error a ConfigurationException is raised.
    """

    config = {
        'use_physical_registers': bool,
        'physical_registers_number': int,
        'allocator_module_location': str,
        'allocator_module_name': str,
        'allocator_function_name': str,
        'physical_registers_prefix': str,
        'spill_virtual_registers_prefix': str,
        'spill_virtual_registers_type': str,
        'param_regs_count': int
    }

    for key in config:
        # dict key matching
        if key not in register_file_configuration:
            raise ConfigurationException('Invalid register file configuration: key {} is missing.'.format(key))

        element = register_file_configuration[key]
        el_type = config[key]

        # dict value's class matching
        if not isinstance(element, el_type):
            raise ConfigurationException('Invalid register file configuration for key {}: type must be {}, {} given.'.format(key, el_type.__name__, element.__class__.__name__))


def create_register_file(register_file_configuration):
    """
    Creates and returns the proper RegisterFile implementation, given the configuration.
    """

    validate_configuration(register_file_configuration)

    if register_file_configuration['use_physical_registers']:
        return PhysicalRegisterFile(register_file_configuration)

    return VirtualRegisterFile()
