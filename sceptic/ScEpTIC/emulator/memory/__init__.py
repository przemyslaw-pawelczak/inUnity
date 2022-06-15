import logging

from ScEpTIC.exceptions import ConfigurationException, MemoryException

from .virtual_gst import GSTUnifier
from .virtual_ram import SRAM, NVM

class Memory:
    """
    This class represents the memory and is in charge of interfacing with it.
    It initializes both SRAM and NVM, accordingly to a given configuration.
    Stack and Heap must be present and can reside only into one RAM at a time, in any combination.
    Global Symbol Table must be present and can reside in SRAM, NVM or both.

    All the memory spaces between stack, heap and global symbol tables are separated.

    Memory has not a maximum dimension, since this simulator is not focused on memory representation.
    In order to get a correct memory representation, I should also put all the things in the stack (saved PC, canaries)
    and I would be bounded to the compiler back-end conversions and architecture-dependent optimizations.

    Not having a memory size, makes difficult to have a continuous memory space such that at a certain address
    the SRAM ends and starts the NVM, but makes possible to test the program for a generic architecture and then verify if
    it fits the arch. memory requirements.
    This is why the SRAM and NVM have overlapping addresses (but will be accessed correctly accordingly to the configuration).

    Having variables in both SRAM and NVM will require a sort of "lookup table", or the data layout should be performed.
    In this implementation, the lookup table for the variables contains also them and extends the stack with some functionalities.
    In this way:
        - There is a better separation between global variables and local stack
        - With the GSTUnifier is easy to access a variable "transparently" (independently if it resides in NVM or SRAM)
        - There is no need to differentiate addresses between SRAM and NVM.
        - Is possible to compare directly a portion (stack, heap, vars) of the NVM and SRAM with a previous dump

    Stack and heap are kept as separated objects (and not directly mapped to the same "memory") because I do not have to deal
    with overflows that causes the stack or heap to be damaged.
    """

    def __init__(self, memory_configuration):
        logging.debug('Initializing main memory.')

        self._validate_memory_configuration(memory_configuration)

        self.address_prefixes = {'stack': '', 'heap': '', 'sram_gst': '', 'nvm_gst': ''}

        # extract base addresses
        stack_base_address = memory_configuration['base_addresses']['stack']
        heap_base_address = memory_configuration['base_addresses']['heap']

        # extract prefixes
        stack_prefix = memory_configuration['prefixes']['stack'] + '-'
        self.address_prefixes['stack'] = stack_prefix

        heap_prefix = memory_configuration['prefixes']['heap'] + '-'
        self.address_prefixes['heap'] = heap_prefix

        # set up stack, heap and gst.
        stack_initialized = False
        heap_initialized = False
        gst_initialized = False

        self.memory_positions = {'stack': None, 'heap': None, 'gst': []}
        
        # Initialize SRAM
        if memory_configuration['sram']['enabled']:
            config = memory_configuration['sram']

            # set initialization variables
            stack_initialized = config['stack']
            heap_initialized = config['heap']
            gst_initialized = config['gst']
            gst_prefix = config['gst_prefix'] + '-'
            self.address_prefixes['sram_gst'] = gst_prefix

            self.sram = SRAM(config['stack'], config['heap'], config['gst'], stack_base_address, heap_base_address, config['gst_base_address'], stack_prefix, heap_prefix, gst_prefix)

            if config['stack']:
                self.memory_positions['stack'] = 'sram'
                
            if config['heap']:
                self.memory_positions['heap'] = 'sram'

            if config['gst']:
                self.memory_positions['gst'].append('sram')

        else:
            self.sram = None

        # Initialize NVM
        if memory_configuration['nvm']['enabled']:
            config = memory_configuration['nvm']
            gst_prefix = config['gst_prefix'] + '-'
            self.address_prefixes['nvm_gst'] = gst_prefix

            if stack_initialized and config['stack']:
                raise MemoryException('Stack cannot reside both in SRAM and NVM.')

            if heap_initialized and config['heap']:
                raise MemoryException('Heap cannot reside both in SRAM and NVM.')

            # adjust initialization variables
            stack_initialized |= config['stack']
            heap_initialized |= config['heap']
            gst_initialized |= config['gst']

            self.nvm = NVM(config['stack'], config['heap'], config['gst'], stack_base_address, heap_base_address, config['gst_base_address'], stack_prefix, heap_prefix, gst_prefix)

            if config['stack']:
                self.memory_positions['stack'] = 'nvm'

            if config['heap']:
                self.memory_positions['heap'] = 'nvm'

            if config['gst']:
                self.memory_positions['gst'].append('nvm')

        else:
            self.nvm = None

        # Verify initializations
        if self.nvm is None and self.sram is None:
            raise MemoryException('RAM not initialized. Please set at least one between SRAM and NVM.')

        if not stack_initialized:
            raise MemoryException('Stack not initialized. Please set it in SRAM or NVM.')

        if not heap_initialized:
            raise MemoryException('Heap not initialized. Please set it in SRAM or NVM.')

        if not gst_initialized:
            raise MemoryException('Global Symbol Table not initialized. Please set it in SRAM, NVM or both.')

        config = memory_configuration['gst']

        # adjust for disabled memories
        if self.sram is None:
            config['default_ram'] = 'NVM'
            config['other_ram_section'] = None

        elif self.nvm is None:
            config['default_ram'] = 'SRAM'
            config['other_ram_section'] = None

        self.gst = GSTUnifier(self, config['default_ram'], config['other_ram_section'])
        
        self.address_dimension = memory_configuration['address_dimension']
        
        logging.info('Main memory initialized.')


    @staticmethod
    def _is_absolute_address(address):
        """
        Returns if an address is a valid absolute one.
        """

        return isinstance(address, str) and '-0x' in address


    @staticmethod
    def _extract_prefix_from_address(address):
        """
        Extracts the prefix of an absolute address.
        """

        if not Memory._is_absolute_address(address):
            raise ValueError('Invalid address')

        prefix = address.split('-0x')

        return prefix[0]+'-'

    
    @staticmethod
    def _extract_relative_address(address):
        """
        Returns the relative address from an absolute address.
        """

        if not Memory._is_absolute_address(address):
            raise ValueError('Invalid address')

        address = address.split('-')

        return int(address[1], 16)


    @staticmethod
    def _parse_absolute_address(address):
        """
        Returns the prefix and the relative address from an absolute one.
        """

        if not Memory._is_absolute_address(address):
            raise ValueError('Invalid address')

        address = address.split('-')

        relative_address = int(address[1], 16)
        prefix = address[0] + '-'

        return prefix, relative_address


    @staticmethod
    def convert_dimension(dimension, dimension_in_bits):
        """
        Converts a dimension from bits to bytes, if dimension_in_bits is True.
        """

        if dimension_in_bits:
            if dimension % 8 != 0:
                raise MemoryException('[Memory] Invalid memory dimension: {} bits. Dimension must be a multiple of a byte (8 bits).'.format(dimension))

            # convert dimension in bytes
            dimension = dimension // 8  # int division

        return dimension


    def add_offset(self, address, offset, offset_in_bits = True):
        """
        Add an offset to an absolute address
        """

        offset = self.stack.convert_dimension(offset, offset_in_bits)

        prefix, relative_address = self._parse_absolute_address(address)
        relative_address = relative_address + offset

        return self._convert_to_absolute_address(prefix, relative_address)


    @staticmethod
    def _convert_to_absolute_address(prefix, address):
        """
        Returns an absolute address, given a prefix
        """

        return '{}{}'.format(prefix, hex(address))


    def write(self, address, dimension, content, dimension_in_bits = True):
        """
        Performs the call to the correct write method.
        """

        prefix = self._extract_prefix_from_address(address)

        if prefix == self.stack.address_prefix:
            return self.stack.write(address, dimension, content, dimension_in_bits)

        elif prefix == self.heap.address_prefix:
            return self.heap.write(address, dimension, content, dimension_in_bits)

        elif prefix in self.gst.address_prefix:
            return self.gst.write(address, dimension, content, dimension_in_bits)

        raise MemoryException('Invalid address {}: prefix not found in memory!'.format(address))


    def set_cell_input_lookup(self, address, input_lookup):
        """
        Sets the input lookup information of cell in a given address.
        """

        # NB: emptiness of input lookup if input_lookup is [] is guaranteed by write operations
        # which removes completely the lookup infos.
        
        if len(input_lookup) == 0:
            return
            
        prefix = self._extract_prefix_from_address(address)
        
        if prefix == self.stack.address_prefix:
            return self.stack.set_cell_input_lookup(address, input_lookup)

        elif prefix == self.heap.address_prefix:
            return self.heap.set_cell_input_lookup(address, input_lookup)

        elif prefix in self.gst.address_prefix:
            return self.gst.set_cell_input_lookup(address, input_lookup)

        raise MemoryException('Invalid address {}: prefix not found in memory!'.format(address))

    
    def get_cell_input_lookup(self, address):
        """
        Returns the input lookup information of cell in a given address.
        """

        prefix = self._extract_prefix_from_address(address)
        
        if prefix == self.stack.address_prefix:
            return self.stack.get_cell_input_lookup(address)

        elif prefix == self.heap.address_prefix:
            return self.heap.get_cell_input_lookup(address)

        elif prefix in self.gst.address_prefix:
            return self.gst.get_cell_input_lookup(address)

        raise MemoryException('Invalid address {}: prefix not found in memory!'.format(address))


    def get_cells_from_address(self, address, dimension, dimension_in_bits = True, resolve_address = True):
        """
        Performs the call to the correct get_cells_from_address method
        """

        prefix = self._extract_prefix_from_address(address)

        if prefix == self.stack.address_prefix:
            return self.stack.get_cells_from_address(address, dimension, dimension_in_bits, resolve_address)

        elif prefix == self.heap.address_prefix:
            return self.heap.get_cells_from_address(address, dimension, dimension_in_bits, resolve_address)

        elif prefix in self.gst.address_prefix:
            return self.gst.get_cells_from_address(address, dimension, dimension_in_bits, resolve_address)

        raise MemoryException('Invalid address {}: prefix not found in memory!'.format(address))


    def set_cells_from_address(self, address, cells, resolve_address = True):
        """
        Performs the call to the correct set_cells_from_address method
        """

        prefix = self._extract_prefix_from_address(address)

        if prefix == self.stack.address_prefix:
            return self.stack.set_cells_from_address(address, cells, resolve_address)

        elif prefix == self.heap.address_prefix:
            return self.heap.set_cells_from_address(address, cells, resolve_address)

        elif prefix in self.gst.address_prefix:
            return self.gst.set_cells_from_address(address, cells, resolve_address)

        raise MemoryException('Invalid address {}: prefix not found in memory!'.format(address))


    def read(self, address, dimension, dimension_in_bits = True):
        """
        Performs the call to the correct read method.
        """

        prefix = self._extract_prefix_from_address(address)

        if prefix == self.stack.address_prefix:
            return self.stack.read(address, dimension, dimension_in_bits)

        elif prefix == self.heap.address_prefix:
            return self.heap.read(address, dimension, dimension_in_bits)

        elif prefix in self.gst.address_prefix:
            return self.gst.read(address, dimension, dimension_in_bits)

        raise MemoryException('Invalid address {}: prefix not found in memory!'.format(address))

    @property
    def stack(self):
        """
        Returns transparently the stack
        Stack must be in sram or nvm.
        If sram not initialized or stack not in sram, it must be in nvm, otherwise
        the memory has not been initialized and an exception have been raised on init.
        """

        if self.sram is not None and self.sram.stack is not None:
            return self.sram.stack

        return self.nvm.stack


    @property
    def heap(self):
        """
        Returns transparently the heap
        Heap must be in sram or nvm.
        If sram not initialized or heap not in sram, it must be in nvm, otherwise
        the memory has not been initialized and an exception have been raised on init.
        """
        
        if self.sram is not None and self.sram.heap is not None:
            return self.sram.heap

        return self.nvm.heap


    def reset(self):
        """
        Performs the CPU reset operation
        """

        logging.debug('Memory reset.')

        if self.sram is not None:
            self.sram.reset()


    def force_nvm_reset(self):
        """
        Resets the NVM.
        """

        if self.nvm is not None:
            self.nvm.force_reset()


    @staticmethod
    def _validate_memory_configuration(memory_configuration):
        """
        Validates a memory configuration dictionary.
        """

        config = {
            'sram': {'enabled': bool, 'stack': bool, 'heap': bool, 'gst': bool, 'gst_prefix': str, 'gst_base_address': int},
            'nvm': {'enabled': bool, 'stack': bool, 'heap': bool, 'gst': bool, 'gst_prefix': str, 'gst_base_address': int},
            'base_addresses': {'stack': int, 'heap': int},
            'prefixes': {'stack': str, 'heap': str},
            'gst': {'default_ram': str, 'other_ram_section': str},
            'address_dimension': int
        }

        # keys must match
        for key in config:
            if key not in memory_configuration:
                raise ConfigurationException('Invalid memory configuration: key {} is missing.'.format(key))

            sub_conf = config[key]
            sub_mem_conf = memory_configuration[key]

            if isinstance(sub_conf, dict):
                # keys of 2nd level dict must match
                for sub_key in sub_conf:
                    if sub_key not in sub_mem_conf:
                        raise ConfigurationException('Invalid memory configuration: subkey {} of key {} is missing.'.format(sub_key, key))

                    sub_type = sub_conf[sub_key]
                    
                    # types must match
                    if not isinstance(sub_mem_conf[sub_key], sub_type):
                        raise ConfigurationException('Invalid memory configuration for subkey {} of key {}: type must be {}, {} given.'.format(sub_key, key, sub_type.__name__, sub_mem_conf[sub_key].__class__.__name__))
            
            elif not isinstance(sub_mem_conf, sub_conf):
                raise ConfigurationException('Invalid memory configuration for key {}: type must be {}, {} given.'.format(key, sub_conf.__name__, sub_mem_conf.__class__.__name__))
