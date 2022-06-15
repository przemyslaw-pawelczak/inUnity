from .emulator.vm import VM

def init(config):
    """
    Initializes ScEpTIC environment
    """

    return VM(config)
