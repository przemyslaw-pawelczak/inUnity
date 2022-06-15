import copy
import logging

from ScEpTIC.exceptions import MemoryException

from .virtual_memory import VirtualMemory, VirtualMemoryCell


class VirtualHeap(VirtualMemory):
    """
    Implementation of the heap.
    """

    def __init__(self, base_address, address_prefix):
        # used on deallocation to deallocate properly groups of cells
        self._memory_groups = {}
        super().__init__(base_address, address_prefix)


    def __eq__(self, other):
        if not isinstance(other, VirtualHeap):
            return False

        return super().__eq__(other) and self._memory_groups == other._memory_groups


    def _get_base_group_address(self, address):
        """
        Returns the address of the first cell of a given group, given an address.
        It is used to deallocate a given group of cells.
        """
        logging.debug('[{}] Getting group base address of {}{}'.format(self.mem_type, self.address_prefix, hex(address)))

        # if at start of memory cell
        if address in self._memory_groups:
            return address

        # if inside memory cell
        for element in self._memory_groups.values():
            if element[0] <= address < element[1]:
                return element[0]

        return None


    def _get_addressable_garbage(self, dimension):
        """
        Returns the address of the first garbage cell which can contain a given dimension of bytes.
        If no such garbage cell is found, it returns None.
        """
        logging.debug('[{}] Getting addressable garbage of size {} bytes'.format(self.mem_type, dimension))

        # dimension is already in bytes
        addresses = sorted(self._memory.keys())

        for addr in addresses:
            cell = self._memory[addr]

            # if marked as garbage, can be reallocated
            if cell.garbage:
                
                if cell.dimension == dimension:
                    cell.garbage = False
                    return cell.address
                
                elif cell.dimension > dimension:
                    self._rebase(cell.address, dimension)
                    cell.garbage = False
                    return cell.address

        return None


    def _get_prev_cell(self, address, raw_access=False):
        """
        Returns a memory cell which is previous of a given address.
        If raw_access is set, the given address can be in the middle of a cell.
        """
        logging.debug('[{}] Getting previous cell of address {}{}{}.'.format(self.mem_type, self.address_prefix, hex(address), ' with raw access' if raw_access else ''))
        indexes = sorted(self._memory.keys())

        try:
            index = indexes.index(address) - 1

        except ValueError:
            if raw_access:
                index = 0

                for i in indexes:
                    if i < address:
                        index = indexes.index(i)

                    else:
                        break

                index = index - 1

            else:
                return None

        if index < 0:
            return None

        prev_addr = indexes[index]
        return self._memory[prev_addr]


    def _get_next_cell(self, address, raw_access=False):
        """
        Returns a memory cell which is previous of a given address.
        If raw_access is set, the given address can be in the middle of a cell.
        """

        logging.debug('[{}] Getting next cell of address {}{}{}.'.format(self.mem_type, self.address_prefix, hex(address), ' with raw access' if raw_access else ''))
        indexes = sorted(self._memory.keys())
        
        try:
            index = indexes.index(address) + 1

        except ValueError:
            if raw_access:
                index = 0

                for i in indexes:
                    if i > address:
                        index = indexes.index(i)
                        break

                index = index + 1
                
            else:
                return None

        if index >= len(indexes):
            return None

        next_addr = indexes[index]
        return self._memory[next_addr]


    def _group_normalize(self, address_group):
        """
        Normalizes an address_group to make it sure that starting and ending cells are not merged with other ones outside
        the memory group.
        """

        logging.debug('[{}] Normalizing memory group {}'.format(self.mem_type, address_group))

        # if top address not in memory, it have been merged with a previous one by a rebase
        if address_group[0] not in self._memory:
            rebase_addr = self._get_cell_base_address(address_group[0])
            
            if rebase_addr is None:
                raise MemoryException('[{}] Unable to perform memory deallocation operation: no memory cell found containing address {}{}'.format(self.mem_type, self.address_prefix, hex(address_group[0])))

            new_dim = address_group[0] - rebase_addr
            
            # perform rebase
            self._rebase(rebase_addr, new_dim)
            # now address is in memory


        # if ending cell is not in memory, some write exceeded its dimension or the memory group is at the end of the HEAP
        if address_group[1] not in self._memory:
            rebase_addr = self._get_cell_base_address(address_group[1])
            # if rebase_addr is not None, there exists some other cell in the HEAP, so rebase is needed
            if rebase_addr is not None:
                new_dim = address_group[1] - rebase_addr
                self._rebase(rebase_addr, new_dim)


    def allocate(self, dimension, dimension_in_bits = True, append_prefix=True):
        """
        Allocates a cell with a given dimension and returns its address.
        It checks for available garbage space, and if it is found the cell will be allocated there.
        """

        dimension = self.convert_dimension(dimension, dimension_in_bits)
        
        address = self._get_addressable_garbage(dimension)

        # if no garbage is addressable for the given dimension, get address of first free space
        # and allocate a new virtual memory cell.
        if address is None:
            address = self.top_address
            cell = VirtualMemoryCell(address, self.address_prefix, dimension)
            self._memory[address] = cell

            # update address of first free space
            self.top_address = self.top_address + dimension

        else:
            cell = self._memory[address]
            self._check_for_memory_map_anomaly(cell)

        cell.collect_memory_trace('allocation')
        cell.set_lookup(None, self._vmstate.register_file.pc, self._vmstate.global_clock, True)

        logging.debug('[{}] Allocating {} bytes at address {}{}.'.format(self.mem_type, dimension, self.address_prefix, hex(address)))
        
        self._memory_groups[address] = (address, address+dimension, dimension)

        if append_prefix:
            return '{}{}'.format(self.address_prefix, hex(address))

        else:
            return address


    def _update_group_lookup(self, group_address):
        """
        Updates the memory group lookup information (memory map).
        """

        address = self._get_base_group_address(group_address)
        address_group = self._memory_groups[address]
        cell = self._memory[address]

        # set memory mapped
        while cell is not None and cell.address < address_group[1]:
            cell.set_memory_mapped(self._vmstate.register_file.pc, self._vmstate.global_clock, cell.address, cell.dimension)
            cell = self._get_next_cell(cell.address)


    def reallocate(self, address, dimension, dimension_in_bits = True, resolve_address=True):
        """
        It reallocates a group of cells to fit a given dimension.
        The address of the first element of the group is returned. (It can change or not)
        """

        dimension = self.convert_dimension(dimension, dimension_in_bits)

        if resolve_address:
            address = self.get_real_address(address)

        logging.debug('[{}] Reallocating {} bytes of memory from address {}{}.'.format(self.mem_type, dimension, self.address_prefix, hex(address)))
        

        base_grp_addr = self._get_base_group_address(address)
        
        if base_grp_addr is None:
            raise MemoryException('[{}] Unable to perform memory reallocation operation: no memory cell found at address {}{}'.format(self.mem_type, self.address_prefix, hex(address)))

        else:
            # address is now the on on the top of the memory group
            address = base_grp_addr

        address_group = self._memory_groups[address]
        self._group_normalize(address_group)

        self._update_group_lookup(address)

        # same dimension, no action needed
        if dimension == address_group[2]:
            return '{}{}'.format(self.address_prefix, hex(address_group[0]))

        # some cells must be removed
        elif dimension < address_group[2]:
            # calculate garbage features
            middle_address = address_group[0] + dimension
            garbage_dimension = address_group[2] - dimension

            # calculate new memory groups
            new_group = (address_group[0], middle_address, dimension)
            garbage_group = (middle_address, address_group[1], garbage_dimension)

            # update memory groups
            self._memory_groups[address] = new_group
            self._memory_groups[middle_address] = garbage_group

            # get containing cell of middle_address
            base_address = self._get_cell_base_address(middle_address)
            cell = self._memory[base_address]
            new_dim = middle_address - cell.address
            
            # if new dimension is < than actual cell dimension, need to rebase
            if base_address != middle_address and new_dim < cell.dimension:
                self._rebase(cell.address, new_dim)

            self.deallocate(middle_address, False)

            return '{}{}'.format(self.address_prefix, hex(new_group[0]))

        # dimension > address_group[2] -> some cells must be added
        else:
            bytes_needed = dimension - address_group[2]
            lookup_address = address_group[1]
            new_group = (address_group[0], address_group[1]+bytes_needed, address_group[2]+bytes_needed)

            # if terminating address of the group is in memory, check if can be extended or must be reallocated
            if lookup_address in self._memory:
                cell = self._memory[lookup_address]

                # next cell is garbage and can be used.
                if cell.garbage and cell.dimension >= bytes_needed:
                    self._rebase(cell.address, bytes_needed)
                    cell.garbage = False
                    self._memory_groups[address_group[0]] = new_group
                    return '{}{}'.format(self.address_prefix, hex(new_group[0]))
                
                # next cell is not garbage. Must reallocate and move values
                else:
                    # dimension already in bytes and do not append prefix
                    new_address = self.allocate(dimension, False, False)
                    top_address = new_address

                    cell = self._memory[address]

                    # copy memory
                    while cell is not None and cell.address < address_group[1]:
                        # dimension in bytes, address explicit.
                        self.write(new_address, cell.dimension, cell.content, False, False)

                        # preserve input lookup information
                        self.set_cell_input_lookup(new_address, copy.deepcopy(cell.get_input_lookup()), False)
                        
                        new_address += cell.dimension
                        cell = self._get_next_cell(cell.address)
                    
                    self.deallocate(address, False)

                    return '{}{}'.format(self.address_prefix, hex(top_address))

            # the cell is at the end of the heap and can be simply incremented
            else:
                cell = VirtualMemoryCell(lookup_address, self.address_prefix, bytes_needed)
                cell.set_lookup(None, self._vmstate.register_file.pc, self._vmstate.global_clock, True)

                self._memory[cell.address] = cell
                self._memory_groups[address_group[0]] = new_group
                self.top_address = new_group[1]

                return '{}{}'.format(self.address_prefix, hex(new_group[0]))

    
    def deallocate(self, address, resolve_address=True):
        """
        Marks as garbage the group of cells containing address.
        It also merges adjacent garbage cells and if the cell is at the end of the heap, simply removes it.
        """

        if resolve_address:
            address = self.get_real_address(address)

        logging.debug('[{}] Deallocating memory at address {}{}.'.format(self.mem_type, self.address_prefix, hex(address)))

        base_grp_addr = self._get_base_group_address(address)

        if base_grp_addr is None:
            raise MemoryException('[{}] Unable to perform memory deallocation operation: no memory cell found at address {}{}'.format(self.mem_type, self.address_prefix, hex(address)))
            
        else:
            # address is now the on on the top of the memory group
            address = base_grp_addr

        address_group = self._memory_groups[address]
        self._group_normalize(address_group)

        # remap group first cell into its max dimension and free it
        cell = self._memory[address]
        old_content = copy.deepcopy(cell.content)
        old_address = cell.address
        old_dimension = cell.dimension
        cell.remap(address_group[2])
        cell.free()
        cell.collect_memory_trace('deallocation')
        cell.set_lookup(old_content, self._vmstate.register_file.pc, self._vmstate.global_clock)
        cell.set_memory_mapped(self._vmstate.register_file.pc, self._vmstate.global_clock, old_address, old_dimension)

        # Remove group cells, except for starting one
        for addr in range(address_group[0]+1, address_group[1]):
            if addr in self._memory:
                self._memory[addr].collect_memory_trace('deallocation')
                del self._memory[addr]

        # remove memory group
        del self._memory_groups[address]

        # get lower cells to check if garbage merging is possible
        prev_cell = self._get_prev_cell(cell.address)

        if prev_cell is not None and prev_cell.garbage:
            new_dim = prev_cell.dimension + cell.dimension
            prev_cell.remap(new_dim)
            
            del self._memory[cell.address]
            cell = prev_cell

            cell.set_memory_mapped(self._vmstate.register_file.pc, self._vmstate.global_clock, old_address, old_dimension)

        next_cell = self._get_next_cell(cell.address)

        if next_cell is None:
            # end of the heap, remove directly the cell
            del self._memory[cell.address]
            self.top_address = cell.address

        elif next_cell is not None and next_cell.garbage:
            # can merge with the next cell
            new_dim = next_cell.dimension + cell.dimension
            
            cell.remap(new_dim)
            cell.set_memory_mapped(self._vmstate.register_file.pc, self._vmstate.global_clock, old_address, old_dimension)

            del self._memory[next_cell.address]


    def restore(self, dump):
        """
        Restores a dump of the heap.
        """

        super().restore(dump)
        self._memory_groups = copy.deepcopy(dump._memory_groups)


    def reset(self):
        """
        Performs the CPU reset operation
        """

        super().reset()
        self._memory_groups = {}
    

    def diff(self, dump):
        """
        Returns the difference between the current state of the register file and the one saved inside a dump.
        """

        diff = super().diff(dump)

        if self._memory_groups != dump._memory_groups:
            mem_keys = list(self._memory_groups.keys())
            dump_keys = list(dump._memory_groups.keys())

            common_elements = [item for item in mem_keys if item in dump_keys]
            only_mem_keys = [item for item in mem_keys if item not in dump_keys]
            only_dump_keys = [item for item in dump_keys if item not in mem_keys]

            for i in common_elements:
                if self._memory_groups[i] != dump._memory_groups[i]:
                    address = '{}{}'.format(self.address_prefix, hex(i))
                    diff.append({'element': '{} memory_group'.format(self.mem_type), 'group_base_address': address, 'dump_value': copy.deepcopy(dump._memory_groups[i]), 'current_value': copy.deepcopy(self._memory_groups[i])})

            for i in only_mem_keys:
                address = '{}{}'.format(self.address_prefix, hex(i))
                diff.append({'element': '{} memory_group'.format(self.mem_type), 'group_base_address': address, 'dump_value': None, 'current_value': copy.deepcopy(self._memory_groups[i])})

            for i in only_dump_keys:
                address = '{}{}'.format(self.address_prefix, hex(i))
                diff.append({'element': '{} memory_group'.format(self.mem_type), 'group_base_address': address, 'dump_value': copy.deepcopy(dump._memory_groups[i]), 'current_value': None})

        return diff
