import logging

from ScEpTIC.exceptions import MemoryException

from .virtual_memory import VirtualMemory, VirtualMemoryCell

class VirtualStack(VirtualMemory):
    """
    Extension of VirtualMemory which represents the stack of the simulated program.
    In this implementation the stack grows from lower to higher addresses.

    Write and read functions are necessary due to the memory allocation method given by LLVM-IR.
    It does not handle the stack: firstly it allocates some space, then it writes to it.

    PUSH and POP operations are to support function calls.
    """
    
    def __eq__(self, other):
        if not isinstance(other, VirtualStack):
            return False

        return super().__eq__(other)
        

    def _get_top_cell_address(self):
        """
        Returns the address of the memory cell in top of the stack.
        """

        logging.debug('[{}] Getting address of cell on top of the stack.'.format(self.mem_type))
        indexes = sorted(self._memory.keys())

        try:
            index = indexes.index(self.top_address)-1

        except ValueError:
            index = -1

        try:
            return indexes[index]

        except ValueError:
            raise MemoryException('[{}] Stack seems to be empty!'.format(self.mem_type))


    def allocate(self, dimension, dimension_in_bits = True, metadata = None):
        """
        Allocates elements on top of the stack.
        """

        dimension = self.convert_dimension(dimension, dimension_in_bits)
        # get address of first free space
        address = self.top_address
        
        logging.debug('[{}] Allocating {} bytes at address {}{}.'.format(self.mem_type, dimension, self.address_prefix, hex(address)))

        if address in self._memory:
            cell = self._memory[address]

            if cell.dimension == dimension:
                cell.metadata = metadata
                # clear tracked data
                cell.other_memory_trace_addresses = []

            elif cell.dimension > dimension:
                # redimensionate cell and create nulled space
                
                # create new cell
                new_cell = VirtualMemoryCell(address, self.address_prefix, dimension)
                new_cell.set_lookup(None, self._vmstate.register_file.pc, self._vmstate.global_clock, True)
                self._memory[address] = new_cell

                # create remaining part of space
                diff_addr = address + dimension
                diff_dim = cell.dimension - dimension
                diff_cell = VirtualMemoryCell(diff_addr, self.address_prefix, diff_dim)
                diff_cell.set_lookup(None, self._vmstate.register_file.pc, self._vmstate.global_clock, True)
                self._memory[diff_addr] = diff_cell

                # For memory trace: in this case, we "allocate" a smaller cell.
                # Allocation in stack happens only on function call, the start memory address remains unchanged
                # so eventual anomalies are still analyzable (we are sizing down)

            else:
                # need more cells
                required_dimension = dimension

                also_track_addresses = []

                # for each element which can start inside the address interval
                for i in range(address, address + dimension):

                    # if a cell exists at such interval
                    if i in self._memory:
                        cell = self._memory[i]
                        
                        # decrement required dimension
                        required_dimension -= cell.dimension
                        
                        # For memory trace: in this case, we "allocate" a bigger cell.
                        # We need to trace the memory access as if a write on the whole cells happened
                        also_track_addresses.append(cell.absolute_address)

                        # remove memory cell
                        del self._memory[i]
                        
                        # if considered cell bigger than required dimension (exceed address + dimension)
                        if required_dimension < 0:
                            diff_addr = cell.address + cell.dimension + required_dimension  # NB: required_dimension is negative!!!
                            diff_dim  = -required_dimension
                            diff_cell = VirtualMemoryCell(diff_addr, self.address_prefix, diff_dim)
                            diff_cell.set_lookup(None, self._vmstate.register_file.pc, self._vmstate.global_clock, True)
                            self._memory[diff_addr] = diff_cell
                            break

                # Here two cases: Required dimension reached or not. If not, top of the modified stack have been reached and space needs to be allocated.
                # If yes, cells are deleted and must be recreated

                new_cell = VirtualMemoryCell(address, self.address_prefix, dimension)
                new_cell.set_lookup(None, self._vmstate.register_file.pc, self._vmstate.global_clock, True)
                self._memory[address] = new_cell
                new_cell.other_memory_trace_addresses = also_track_addresses

            self._memory[address].metadata = metadata

            self.top_address = self.top_address + dimension
            return '{}{}'.format(self.address_prefix, hex(address))
            
        return self._allocate(dimension, False, metadata)

    def deallocate(self, address, resolve_address = True, ignore_exception = False):
        """
        Decrements the ESP (-> deallocation all the cells until a given address).
        It doesn't really remove data.
        """

        if resolve_address:
            address = self.get_real_address(address)

        logging.debug('[{}] Deallocating memory starting from address {}{}.'.format(self.mem_type, self.address_prefix, hex(address)))

        if address not in self._memory:
            
            if ignore_exception:
                return

            raise MemoryException('[{}] Unable to perform memory deallocation operation: no memory cell starts at {}'.format(self.mem_type, address))

        self.top_address = address
    

    def _allocate(self, dimension, dimension_in_bits = True, metadata = None):
        """
        Allocates a single cell in top of the stack with a given dimension, and returns the address.
        (PUSH-like)
        """

        dimension = self.convert_dimension(dimension, dimension_in_bits)
        # get address of first free space
        address = self.top_address
        
        logging.debug('[{}] Allocating {} bytes at address {}{}.'.format(self.mem_type, dimension, self.address_prefix, hex(address)))

        # allocate space
        cell = VirtualMemoryCell(address, self.address_prefix, dimension)
        cell.set_lookup(None, self._vmstate.register_file.pc, self._vmstate.global_clock, True)
        cell.metadata = metadata

        # append to memory
        self._memory[address] = cell

        # update address of first free space
        self.top_address = self.top_address + dimension

        return '{}{}'.format(self.address_prefix, hex(address))


    def _deallocate(self, address, resolve_address = True, ignore_exception = False):
        """
        Deallocates all the cells until address. Is used to remove the cells in top of the stack.
        (POP-like)
        """

        if resolve_address:
            address = self.get_real_address(address)

        logging.debug('[{}] Deallocating memory starting from address {}{}.'.format(self.mem_type, self.address_prefix, hex(address)))
        
        if address not in self._memory:

            if ignore_exception:
                return
                
            raise MemoryException('[{}] Unable to perform memory deallocation operation: no memory cell starts at {}. {}'.format(self.mem_type, address, sorted(self._memory.keys())))

        # use list(...) to avoid RuntimeError: dictionary changed size during iteration
        for addr in list(self._memory.keys()):
            if addr >= address:
                logging.debug('[{}] Deallocating memory cell at address {}{} ({} bytes).'.format(self.mem_type, self.address_prefix, hex(addr), self._memory[addr].dimension))
                del self._memory[addr]

        self.top_address = address


    def _set_metadata(self, address, metadata):
        """
        Sets metadata information to help finding anomalies in stack.
        """

        address = self.get_real_address(address)
        self._memory[address].metadata = metadata


    def push(self, dimension, content, metadata = None, dimension_in_bits = True):
        """
        Push a given value on top of the stack
        """

        address = self.allocate(dimension, dimension_in_bits, metadata)
        self.write(address, dimension, content, dimension_in_bits)

        # metadata info for stack anomalies
        if metadata is not None:
            self._set_metadata(address, metadata)


    def pop(self, dimension, dimension_in_bits = True):
        """
        Pops the value on the top of the stack
        """

        address = self._get_top_cell_address()
        
        # address is the real one
        value = self.read(address, dimension, dimension_in_bits, False)
        
        self.deallocate(address, False)

        return value
