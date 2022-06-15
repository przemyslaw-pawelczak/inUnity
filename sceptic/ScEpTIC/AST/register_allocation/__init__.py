import logging

def get_register_allocator(module_location, module_name, allocation_function_name):
    """
    Function that dynamically loads the requested register allocation module and returns its main function,
    to be used to perform it.
    """

    logging.debug('[RegisterAllocation] from {}.{} import {}'.format(module_location, module_name, allocation_function_name))

    # set absolute module name
    module_name = '{}.{}'.format(module_location, module_name)

    # import the corresponding module
    module = __import__(module_name, fromlist=[allocation_function_name])

    # return requested function
    return getattr(module, allocation_function_name)
