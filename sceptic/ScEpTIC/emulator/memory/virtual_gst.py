import copy
import logging

from ScEpTIC.exceptions import MemoryException

from .virtual_stack import VirtualStack


class VirtualGlobalSymbolTable(VirtualStack):
    """
    This class extends the stack and will contains only symbols (the global variables).
    Even if this section could be put in top of the stack, given the fact that both SRAM and NVM
    can exists, I need a simple way to find global variables without inspecting the stack of the SRAM and
    the memory of the NVM.
    It just contains a dictionary of global variables that associates them to their address in the "stack".

    """

    def __init__(self, base_address, address_prefix):
        self._global_vars = {}
        self._cells_no = {}
        self._base_state = {'memory': None, 'global_vars': None, 'top_address': None}
        super().__init__(base_address, address_prefix)


    def __eq__(self, other):
        if not isinstance(other, VirtualGlobalSymbolTable):
            return False

        return super().__eq__(other) and self._global_vars == other._global_vars


    def _get_symbol_address(self, name, absolute_address = False):
        """
        Returns the address of a symbol, given its name.
        """
        logging.debug('[{}] Resolving address of symbol {}.'.format(self.mem_type, name))

        if not self.has_symbol(name):
            raise MemoryException('[{}] Unable to find symbol {}!'.format(self.mem_type, name))

        address = self._global_vars[name]

        if absolute_address:
            return '{}{}'.format(self.address_prefix, hex(address))

        return address
    

    def allocate(self, name, composition, initial_values, dimension_in_bits = True):
        """
        Allocates the required space for a given symbol name.
        The space is allocated accordingly to the given composition, which is a list of lists.
        Each element of the list is a sublist containing the number of elements and their dimension.
        It returns the address of the first allocated cell of the symbol.
        """

        if self.has_symbol(name):
            raise MemoryException('[{}] Symbol {} already present!'.format(self.mem_type, name))

        base_address = self.top_address

        logging.debug('[{}] Allocating space for symbol {} at address {}.'.format(self.mem_type, name, hex(base_address)))

        self._global_vars[name] = base_address
        self._cells_no[name] = len(composition)

        for i in range(0, len(composition)):
            dimension = composition[i]

            addr = super().allocate(dimension, dimension_in_bits, 'Global variable {}'.format(name))

            if initial_values is not None:

                if i >= len(initial_values):
                    initial_val = None

                else:
                    initial_val = initial_values[i]
                
                self.write(addr, dimension, initial_val, dimension_in_bits)

        # return base address of symbol
        return '{}{}'.format(self.address_prefix, base_address)


    def read_string_from_address(self, address):
        """
        Reads a string from a memory address
        """

        address = self.get_real_address(address)
        symbol_name = self._get_symbol_name_from_address(address)
        symbol_len = self._cells_no[symbol_name]

        content = ''

        for index in range(0, symbol_len):
            val = self._memory[address + index].content

            if val is not None and val > 0:
                content += chr(val)

        return content


    def deallocate(self, address):
        """
        Deallocation not supported for this memory type.
        """

        raise MemoryException('[{}] Memory operation not allowed!'.format(self.mem_type))


    def has_symbol(self, name):
        """
        Returns if a given symbol is in the VirtualGlobalSymbolTable
        """
        return name in self._global_vars


    def read_from_symbol_name(self, name, dimension, dimension_in_bits = True):
        """
        Returns the value of a symbol, given its name and dimension.
        The request is "forwared" to the stack's read function, after having calculated the needed address.
        """
        logging.debug('[{}] Reading symbol {}.'.format(self.mem_type, name))
        
        address = self._get_symbol_address(name)

        return self.read(address, dimension, dimension_in_bits, False)


    def write_from_symbol_name(self, name, dimension, content, dimension_in_bits = True):
        """
        Writes the given value to the specified symbol, given its name and dimension.
        The request is "forwared" to the stack's write function, after having calculated the needed address.
        """
        logging.debug('[{}] Writing symbol {} with content {}.'.format(self.mem_type, name, content))
        
        address = self._get_symbol_address(name)

        return self.write(address, dimension, content, dimension_in_bits, False)


    def get_visual_dump(self, head_string):
        """
        Returns a string representing the memory
        """
        dump = '('+head_string+')\n'+str(self)+"\n"

        for var in sorted(self._global_vars.keys()):
            address = self._global_vars[var]
            content = self._memory[address].content
            address = self._get_symbol_address(var, True)
            dump += '[{}] {}: {}\n'.format(address, var, content)

        return dump
    
    
    def restore(self, dump):
        """
        Restores a dump of the heap.
        """

        super().restore(dump)
        self._global_vars = copy.deepcopy(dump._global_vars)


    def reset(self):
        """
        Performs the CPU reset operation
        """

        self._global_vars = copy.deepcopy(self._base_state['global_vars'])
        self._memory = copy.deepcopy(self._base_state['memory'])
        self.top_address = copy.deepcopy(self._base_state['top_address'])


    def set_state_as_base_state(self):
        """
        Sets the current state as the base state, which is the one restored when reset() is called.
        """

        self._base_state['global_vars'] = copy.deepcopy(self._global_vars)
        self._base_state['memory'] = copy.deepcopy(self._memory)
        self._base_state['top_address'] = copy.deepcopy(self.top_address)


    def _get_symbol_name_from_address(self, address):
        """
        Returns the symbol name given its address.
        """
        candidate = None
        candidate_addr = -1

        for i in self._global_vars:
            addr = self._global_vars[i]
            
            if addr == address:
                return i

            elif candidate_addr < addr < address:
                candidate = i
                candidate_addr = addr

        return candidate


    def diff(self, dump):
        """
        Returns the difference between the current state of the register file and the one saved inside a dump.
        """

        logging.debug('[{}] Comparing current state with a given dump.'.format(self.mem_type))

        if not isinstance(dump, self.__class__):
            raise MemoryException('Unable to compare {} dump: {} object expected, {} given.'.format(self.mem_type, self.mem_type, dump.__class__.__name__))

        diff = []

        # NB: global variables are allocated before running the program, so the runtime state cannot differ in terms of number of global variables
        if self._memory != dump._memory:
            mem_keys = list(self._memory.keys())
            dump_keys = list(dump._memory.keys())

            common_elements = [item for item in mem_keys if item in dump_keys]
            only_mem_keys = [item for item in mem_keys if item not in dump_keys]
            only_dump_keys = [item for item in dump_keys if item not in mem_keys]

            for i in common_elements:
                if self._memory[i] != dump._memory[i]:
                    address = '{}{}'.format(self.address_prefix, hex(i))
                    diff.append({'var_name': '{}'.format(self._get_symbol_name_from_address(i)), 'address': address, 'dump_value': dump._memory[i].content, 'current_value': self._memory[i].content})

            for i in only_mem_keys:
                address = '{}{}'.format(self.address_prefix, hex(i))
                diff.append({'var_name': '{}'.format(self._get_symbol_name_from_address(i)), 'address': address, 'dump_value': None, 'current_value': self._memory[i].content})

            for i in only_dump_keys:
                address = '{}{}'.format(self.address_prefix, hex(i))
                diff.append({'var_name': '{}'.format(self._get_symbol_name_from_address(i)), 'address': address, 'dump_value': dump._memory[i].content, 'current_value': None})

        return diff


class GSTUnifier:
    """
    Interface used to interact transparently with one or two Global Symbol Tables.
    It directly interfaces with the memory, in order to get the require gst.
    It does not retain memory information, just interfaces with it.

    The default_ram states which RAM will be used to store variables when section is not specified or
    is not other_ram_section, which is used to identify variables to be stored in the RAM complementary to
    default_ram.
    """

    def __init__(self, memory, default_ram, other_ram_section):
        if not self._is_valid_memory_name(default_ram):
            raise MemoryException('Invalid name \'{}\' for GST default memory location.'.format(default_ram))
        
        self._memory = memory
        self._default_ram = default_ram
        self._other_ram = self._get_other_ram_name(default_ram)
        self._other_ram_section = other_ram_section
        self.address_prefix = []
        
        # GST Must be initialized for default RAM
        default_ram = self._get_ram_from_ram_name(self._default_ram)
        
        if default_ram is None or default_ram.gst is None:
            raise MemoryException('GST not initialized for {}.'.format(self._default_ram))

        self.address_prefix.append(default_ram.gst.address_prefix)
        
        # GST Must be initialized if other_ram_section is not None
        if self._other_ram_section is not None:
            other_ram = self._get_ram_from_ram_name(self._other_ram)

            if other_ram is None or other_ram.gst is None:
                raise MemoryException('GST not initialized for {}.'.format(self._other_ram))

            self.address_prefix.append(other_ram.gst.address_prefix)

        logging.debug('GSTUnifier initialized.')


    @staticmethod
    def _is_valid_memory_name(memory_name):
        """
        Returns if a memory name is valid.
        """

        return memory_name in ['SRAM', 'NVM']


    @staticmethod
    def _get_other_ram_name(name):
        """
        Returns the name of the "complementary" memory.
        SRAM -> NVM
        NVM -> SRAM
        """

        return 'NVM' if name == 'SRAM' else 'SRAM'


    def _get_ram_from_ram_name(self, name):
        """
        Returns the ram corresponding to the given name.
        """
        return self._memory.sram if name == 'SRAM' else self._memory.nvm


    def _get_gst_from_ram_name(self, name):
        """
        Returns the gst corresponding to the given ram name.
        """
        ram = self._get_ram_from_ram_name(name)
        return ram.gst if ram is not None else None


    def _get_gst_from_section(self, section):
        """
        Returns the gst corresponding to the given section name.
        """
        logging.debug('Selecting GST for section {}'.format(section))
        
        # if section not set, only one ram used for gst
        if self._other_ram_section is None:
            return self.default_gst

        # default memory
        if section is None or section != self._other_ram_section:
            return self.default_gst

        return self.other_gst


    def _get_gst_from_symbol(self, name):
        """
        Returns the gst containing a given symbol name.
        """
        logging.debug('Selecting GST for symbol {}'.format(name))
        
        if self.default_gst.has_symbol(name):
            return self.default_gst

        elif self.other_gst is not None and self.other_gst.has_symbol(name):
            return self.other_gst

        raise MemoryException('Symbol {} not found!'.format(name))


    def _get_gst_from_address(self, address):
        """
        Returns the gst containing a given address.
        """
        logging.debug('Selecting GST for address {}'.format(address))

        if self.default_gst.address_prefix in address:
            return self.default_gst

        elif self.other_gst is not None and self.other_gst.address_prefix in address:
            return self.other_gst

        raise MemoryException('Invalid address {}!'.format(address))


    def get_symbol_address(self, name):
        """
        Returns the absolute address of a given symbol.
        """
        logging.debug('Getting address of symbol {}.'.format(name))

        gst = self._get_gst_from_symbol(name)

        return gst._get_symbol_address(name, True)

    def get_address_symbol(self, address):
        """
        Returns the symbol name from a given address.
        """
        logging.debug('Getting symbol of address {}.'.format(address))
        
        try:
            gst = self._get_gst_from_address(address)
            address = gst.get_real_address(address)
            return gst._get_symbol_name_from_address(address)

        except MemoryException:
            return None


    @property
    def default_gst(self):
        """
        Returns the gst of the default ram.
        """
        return self._get_gst_from_ram_name(self._default_ram)


    @property
    def other_gst(self):
        """
        Returns the gst of the complementary ram.
        """
        if self._other_ram_section is None:
            return None

        return self._get_gst_from_ram_name(self._other_ram)
    

    def has_symbol(self, name):
        """
        Returns if a symbol is in any gst.
        """
        return self.default_gst.has_symbol(name) or (self.other_gst is not None and self.other_gst.has_symbol(name))


    def allocate(self, name, section, composition, initial_values, dimension_in_bits=True):
        """
        Allocates the symbol accordingly to the given section.
        If section is None, it allocates it to the default gst.
        """

        # get the proper ram for allocation
        gst = self._get_gst_from_section(section)

        return gst.allocate(name, composition, initial_values, dimension_in_bits)


    def deallocate(self, address):
        """
        Deallocation not possible in gst.
        """
        raise MemoryException('Memory operation not allowed for Global Symbol Table!')


    def read_from_symbol_name(self, name, dimension, dimension_in_bits=True):
        """
        Calls read method of the gst in which the symbol is.
        """
        address = self.get_symbol_address(name)
        return self.read(address, dimension_in_bits, dimension_in_bits)
        

    def write_from_symbol_name(self, name, dimension, content, dimension_in_bits=True):
        """
        Calls write method of the gst in which the symbol is.
        """

        address = self.get_symbol_address(name)
        return self.write(address, dimension, content, dimension_in_bits)


    def read(self, address, dimension, dimension_in_bits = True):
        """
        Reads a symbol cell's content from the GST.
        """

        gst = self._get_gst_from_address(address)
        return gst.read(address, dimension, dimension_in_bits)


    def write(self, address, dimension, content, dimension_in_bits = True):
        """
        Writes into a symbol cell.
        """

        gst = self._get_gst_from_address(address)
        return gst.write(address, dimension, content, dimension_in_bits)


    def get_visual_dump(self):
        """
        Returns a string representing the memory
        """

        dump = self.default_gst.get_visual_dump(self._default_ram)+"\n\n"

        if self.other_gst is not None:
            dump += self.other_gst.get_visual_dump(self._other_ram)

        return dump

    def get_cells_from_address(self, address, dimension, dimension_in_bits = True, resolve_address = True):
        """
        Performs the call to the correct get_cells_from_address method
        """

        gst = self._get_gst_from_address(address)
        return gst.get_cells_from_address(address, dimension, dimension_in_bits, resolve_address)


    def set_cells_from_address(self, address, cells, resolve_address = True):
        """
        Performs the call to the correct set_cells_from_address method
        """

        gst = self._get_gst_from_address(address)
        return gst.set_cells_from_address(address, cells, resolve_address)

    
    def set_state_as_base_state(self):
        """
        Sets the current state as the base state, which is the one restored when reset() is called.
        """

        sram_gst = self._get_gst_from_ram_name('SRAM')
        
        if sram_gst is not None:
            sram_gst.set_state_as_base_state()

        nvm_gst = self._get_gst_from_ram_name('NVM')
        
        if nvm_gst is not None:
            nvm_gst.set_state_as_base_state()


    def set_cell_input_lookup(self, address, input_lookup):
        """
        Sets the input lookup information of cell in a given address.
        """

        # NB: emptiness of input lookup if input_lookup is [] is guaranteed by write operations
        # which removes completely the lookup infos.
        
        if len(input_lookup) == 0:
            return
        
        gst = self._get_gst_from_address(address)

        return gst.set_cell_input_lookup(address, input_lookup)

    
    def get_cell_input_lookup(self, address):
        """
        Returns the input lookup information of cell in a given address.
        """

        gst = self._get_gst_from_address(address)
        return gst.get_cell_input_lookup(address)
