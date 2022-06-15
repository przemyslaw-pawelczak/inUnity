import copy
import logging

from ScEpTIC.exceptions import MemoryException

from .virtual_gst import VirtualGlobalSymbolTable
from .virtual_heap import VirtualHeap
from .virtual_stack import VirtualStack

class VirtualRAM:
    """
    RAM base object. It may contains a stack, a heap and a global symbol table.
    """

    def __init__(self, has_stack, has_heap, has_gst, stack_base_address = 0, heap_base_address = 0, gst_base_address = 0, stack_prefix = 'S-', heap_prefix = 'H-', gst_prefix = 'GST-'):
        logging.debug('Creating {} memory.'.format(self.ram_type))

        if has_stack:
            self.stack = VirtualStack(stack_base_address, stack_prefix)

        else:
            self.stack = None
        
        if has_heap:
            self.heap = VirtualHeap(heap_base_address, heap_prefix)

        else:
            self.heap = None

        if has_gst:
            self.gst = VirtualGlobalSymbolTable(gst_base_address, gst_prefix)

        else:
            self.gst = None


    @property
    def ram_type(self):
        """
        Returns the name of the RAM.
        """

        return self.__class__.__name__


    def reset(self):
        """
        Performs the CPU reset operation
        """

        logging.info('Resetting {}'.format(self.ram_type))

        if self.stack is not None:
            self.stack.reset()

        if self.heap is not None:
            self.heap.reset()

        if self.gst is not None:
            self.gst.reset()

class SRAM(VirtualRAM):
    """
    Static RAM.
    """

    pass


class NVM(VirtualRAM):
    """
    Non Volatile Memory.
    """

    def reset(self):
        """
        NVM is persistent w.r.t. CPU reset
        """

        return

    def force_reset(self):
        """
        Forces reset of NVM
        """

        super().reset()
