import collections
import copy
import logging

from ScEpTIC import tools
from ScEpTIC.emulator.intermittent_executor.anomalies import WARAnomaly, MemoryMapAnomaly, InputPolicyAnomaly
from ScEpTIC.emulator.io.input import InputManager
from ScEpTIC.exceptions import MemoryException, RuntimeException

class MemoryAccessTrace:
    """
    Class representing an operation performed over a memory cell
    """

    def __init__(self, clock, pc, address, value, dimension, op_type, metadata):
        self.clock = clock
        self.pc = copy.deepcopy(pc)
        self.pc_tree = pc.pc_tree()
        self.address = address
        self.value = copy.deepcopy(value)
        self.dimension = dimension
        self.op_type = op_type
        self.metadata = metadata


    def __str__(self):
        return '{}({}) {} {} {}'.format(self.address, self.dimension, self.value, self.pc.resolve(), '' if self.metadata is None else '({})'.format(self.metadata))


    def __repr__(self):
        return self.__str__()


class VirtualMemoryCell:
    """
    Class that represents a single memory cell.
    Cells do not have a fixed dimension, but each cell refers to a single element (e.g. valirable)
    """

    _vmstate = None

    def __init__(self, address, address_prefix, dimension, content = None, garbage = False):
        self.address = address
        self.address_prefix = address_prefix
        self.dimension = dimension
        self.content = content
        self.garbage = garbage
        self.metadata = None
        self._init_lookup()
        self.other_memory_trace_addresses = []

        logging.debug('created {}'.format(repr(self)))
    

    def _init_lookup(self):
        """
        Inits/resets the lookup table of the memory cell.
        """

        self.lookup = {'old_content': None, 'write_pc': None, 'write_global_clock': -1, 'memory_mapped': -1, 'memory_mapped_pc': None, 'input': tools.build_input_lookup_data(None, None)}


    def remap(self, dimension):
        """
        Remaps the dimension of the cell and invalidates the cell content.
        """

        logging.debug('Remapping cell at address {} with dimension {} bytes.'.format(hex(self.address), dimension))
        self.dimension = dimension
        self._init_lookup()
        self.content = None


    def free(self):
        """
        Frees the cell like it is done with C function "free"
        """

        logging.debug('Memory cell at address {} freed.'.format(hex(self.address)))
        self._init_lookup()
        self.content = None
        self.garbage = True


    def set_lookup(self, old_content, current_pc, current_clock, memory_mapped = False):
        """
        Sets lookup informations for memory anomaly checks.
        """

        if not self._vmstate.do_data_anomaly_check:
            return

        self.lookup['old_content'] = old_content
        self.lookup['write_pc'] = copy.deepcopy(current_pc)
        self.lookup['write_global_clock'] = current_clock
        
        if memory_mapped:
            self.set_memory_mapped(current_pc, current_clock, self.address, self.dimension)
        

    def set_input_lookup(self, input_lookup_data):
        """
        Sets the input lookup information of the cell.
        """

        self.lookup['input'] = input_lookup_data


    def get_input_lookup(self):
        """
        Returns the input lookup information of the cell.
        """

        return self.lookup['input']


    def set_memory_mapped(self, current_pc, current_clock, old_memory_address, old_dimension):
        """
        Sets lookup informations for memory anomaly checks.
        """

        self.lookup['memory_mapped_pc'] = copy.deepcopy(current_pc)
        self.lookup['memory_mapped'] = current_clock
        self.lookup['old_memory_address'] = old_memory_address
        self.lookup['old_dimension'] = old_dimension


    @property
    def absolute_address(self):
        """
        Returns the absolute address of the cell
        """

        return "{}{}".format(self.address_prefix, hex(self.address))
    

    def __str__(self):
        return '[{}{} - {}{} ({} bytes)] {}{}'.format(self.address_prefix, hex(self.address), self.address_prefix, hex(self.address+self.dimension-1),
                                                      self.dimension, self.content, ' {GARBAGE}' if self.garbage else '')


    def __repr__(self):
        return 'VirtualMemoryCell({}{}, {}, {}, {})'.format(self.address_prefix, hex(self.address), self.dimension, self.content, self.garbage)


    def __eq__(self, other):
        if not isinstance(other, VirtualMemoryCell):
            return False

        return self.address == other.address and self.address_prefix == other.address_prefix and self.dimension == other.dimension and self.content == other.content and self.garbage == other.garbage and self.lookup == other.lookup


    def collect_memory_trace(self, op_type):
        # If ScEpTIC not set to collect memory traces, skip
        if not self._vmstate.collect_memory_trace:
            return

        # If memory cell not in memory_trace_prefixes (i.e. not in NVM)
        if self.address_prefix not in self._vmstate.memory_trace_prefixes:
            return

        if op_type not in ['read', 'write', 'allocation', 'deallocation']:
            raise RuntimeException('Wrong operation type for memory trace!')

        # Create memory trace
        addr = self.absolute_address
        clock = self._vmstate.global_clock

        # Adjust for deallocation
        dimension = self.dimension if op_type != 'deallocation' else None
        traced_address = addr if op_type != 'deallocation' else None

        if traced_address is None:
            self.metadata = 'Memory address {}'.format(addr)

        memory_trace = MemoryAccessTrace(clock, self._vmstate.register_file.pc, traced_address, self.content, dimension, op_type, self.metadata)
        
        addresses = [addr]

        # on write propagate also write operations that exceeds original cell boundaries
        if op_type == 'write':
            addresses = addresses + self.other_memory_trace_addresses

        for addr in addresses:
            # Create data structure, if needed
            if addr not in self._vmstate.memory_trace:
                self._vmstate.memory_trace[addr] = {'read': collections.OrderedDict(), 'write': collections.OrderedDict(), 'allocation': collections.OrderedDict(), 'deallocation': collections.OrderedDict()}

            # Add memory trace to collected memory traces
            self._vmstate.memory_trace[addr][op_type][clock] = memory_trace


class VirtualMemory:
    """
    Basic representation of the memory.
    It contains cells inside the dictionary _memory (the keys are the initial addresses of each cell)
    """

    _vmstate = None

    def __init__(self, base_address, address_prefix):
        logging.debug('Creating {} memory space starting at address {}{}.'.format(self.__class__.__name__, address_prefix, hex(base_address)))
        
        if base_address < 0:
            raise MemoryException('[{}] Base address {} not valid! It must be >= 0.'.format(self.__class__.__name__, base_address))

        self.base_address = base_address
        self.top_address = base_address
        self.address_prefix = address_prefix
        self._memory = {}


    def __str__(self):
        dimension = self.top_address - self.base_address
        return 'Virtual Memory: {}\nStarting address: {}{}\nEnding address: {}{}\nAllocated cells: {}\nOccupied memory: {} bytes'.format(self.mem_type, self.address_prefix, hex(self.base_address), self.address_prefix, hex(self.top_address), len(self._memory), dimension)


    def __eq__(self, other):
        if not isinstance(other, VirtualMemory):
            return False
            
        return self.base_address == other.base_address and self.address_prefix == other.address_prefix and self.top_address == other.top_address and self._memory == other._memory


    def get_visual_dump(self):
        """
        Returns a string representing the memory
        """

        dump = ''

        for i in sorted(self._memory.keys()):
            dump += str(self._memory[i])+"\n"

        if len(dump) == 0:
            dump = '\n'

        return dump


    def dump(self):
        """
        Returns a dump of the virtual memory.
        """

        logging.debug('Creating dump of {}.'.format(self.mem_type))

        return copy.deepcopy(self)
    

    def restore(self, dump):
        """
        Restores a dump of the virtual memory.
        """

        logging.debug('Restoring dump of {}.'.format(self.mem_type))

        if not isinstance(dump, self.__class__):
            raise MemoryException('Unable to restore {} dump: {} object expected, {} given.'.format(self.mem_type, self.mem_type, dump.__class__.__name__))

        self.top_address = copy.deepcopy(dump.top_address)
        self._memory = copy.deepcopy(dump._memory)
    

    def reset(self):
        """
        Performs the CPU reset operation
        """

        logging.info('Resetting {}'.format(self.mem_type))

        self.top_address = self.base_address
        self._memory = {}


    @property
    def mem_type(self):
        """
        Returns the class of the memory. VirtualMemory is extended by other memory representations.
        """

        return self.__class__.__name__


    def convert_dimension(self, dimension, dimension_in_bits):
        """
        Converts a dimension from bits to bytes, if dimension_in_bits is True.
        """

        if dimension_in_bits:
            if dimension % 8 != 0:
                raise MemoryException('[{}] Invalid memory dimension: {} bits. Dimension must be a multiple of a byte (8 bits).'.format(self.mem_type, dimension))

            # convert dimension in bytes
            dimension = dimension // 8  # int division

        return dimension


    def get_real_address(self, address):
        """
        Returns the actual address (in integer) by removing the address prefix char.
        """

        try:
            address = address.replace(self.address_prefix, '')
            # address is in hex
            return int(address, 16)

        except (ValueError, AttributeError):
            raise MemoryException('[{}] Invalid address {}. Address must start with {} and must be in hex format.'.format(self.mem_type, address, self.address_prefix))


    def _get_cell_base_address(self, address):
        """
        Returns the start address of cell given its address (which can be the starting one or inside it).
        """

        logging.debug('[{}] Getting cell base address of {}{}'.format(self.mem_type, self.address_prefix, hex(address)))

        # if at start of memory cell
        if address in self._memory:
            return address

        # if inside memory cell
        for addr in self._memory:
            cell = self._memory[addr]

            if cell.address < address < (cell.address + cell.dimension):
                return cell.address

        return None


    def _rebase(self, address, dimension):
        """
        Given an address, it redimansionates a cell to fit a given dimension.
        """

        logging.debug('[{}] Rebasing address {}{} to {} bytes.'.format(self.mem_type, self.address_prefix, hex(address), dimension))

        # dimension is already in bytes
        if dimension < 1:
            raise MemoryException('[{}] Unable to perform memory rebasing operation: invalid dimension {}'.format(self.mem_type, dimension))

        if address not in self._memory:
            raise MemoryException('[{}] Unable to perform memory rebasing operation: no memory cell starts at address {}{}'.format(self.mem_type, self.address_prefix, hex(address)))

        cell = self._memory[address]
        old_address = cell.address
        old_dimension = cell.dimension

        if cell.dimension == dimension:
            cell.set_memory_mapped(self._vmstate.register_file.pc, self._vmstate.global_clock, old_address, old_dimension)
            # no actual remap
            return

        elif dimension < cell.dimension:
            # cell must be downsized.
            # find the address from which the cell is not used, and its dimension
            new_addr = cell.address + dimension
            new_dim  = cell.dimension - dimension
            
            # create and apped the cell to the memory
            unused_space = VirtualMemoryCell(new_addr, cell.address_prefix, new_dim, None, cell.garbage)
            unused_space.set_lookup(None, self._vmstate.register_file.pc, self._vmstate.global_clock, True)

            self._memory[new_addr] = unused_space
            
        else:
            # The cell must become bigger
            needed_dim = dimension - cell.dimension
            next_addr = cell.address + cell.dimension

            while needed_dim > 0:
            
                if next_addr not in self._memory:
                    raise MemoryException('[{}] Memory Overflow: unable to extend address {}{} to {} bytes. No cell spaces available.'.format(self.mem_type, self.address_prefix, hex(address), dimension))

                tmp_cell = self._memory[next_addr]
                
                # if tmp_cell is bigger than needed_dim, just rebase it and stop
                # otherwise, update needed_dim and next_address
                if tmp_cell.dimension > needed_dim:
                    self._rebase(tmp_cell.address, needed_dim)
                    needed_dim = 0

                else:
                    needed_dim = needed_dim - tmp_cell.dimension
                    next_addr = tmp_cell.address + tmp_cell.dimension
                
                # Collect memory trace for remapping cell
                tmp_cell.collect_memory_trace('deallocation')

                # remove tmp_cell from memory (will be "inglobated" by cell)
                del self._memory[tmp_cell.address]

        # remap cell to wanted dimension
        cell.remap(dimension)
        cell.collect_memory_trace('allocation')
        cell.set_memory_mapped(self._vmstate.register_file.pc, self._vmstate.global_clock, old_address, old_dimension)


    def _check_input_lookup(self, cell):
        """
        Verifies the input lookup for input anomalies for a given cell.
        """

        if not self._vmstate.input_lookup_enabled:
            return None

        checkpoint_clock = self._vmstate.checkpoint_clock

        # get lookup info from memory cell
        input_lookup_data = cell.get_input_lookup()

        # checkpoint_clock: [list_of_dependencies]
        for clock_id in sorted(input_lookup_data.keys()):

            # consistency observed
            measured_consistency = InputManager.LONG_TERM if clock_id < checkpoint_clock else InputManager.MOST_RECENT

            for input_name in input_lookup_data[clock_id]:
                consistency = InputManager.get_consistency_model(input_name)
                
                # if no consistency is set for considered input, skip
                if consistency is None:
                    continue

                if consistency != measured_consistency:
                    checkpoint_pc = self._vmstate.checkpoint_clock_pc_maps[clock_id]
                    access_pc = self._vmstate.register_file.pc
                    anomaly = InputPolicyAnomaly(checkpoint_pc, checkpoint_clock, access_pc, clock_id, input_name, measured_consistency, consistency)
                    
                    if anomaly not in self._vmstate.anomalies:
                        self._vmstate.anomalies.append(anomaly)
                        
                        # stats
                        self._vmstate.stats.anomaly_found()
                        
                        # Stop test if user requires it
                        self._vmstate.handle_stop_request(anomaly)


    def _check_for_memory_map_anomaly(self, cell):
        """
        Checks for memory mapping anomalies for a given cell.
        """

        if not self._vmstate.do_data_anomaly_check:
            return None

        if cell.address_prefix not in self._vmstate.memory_trace_prefixes or cell.address_prefix != self._vmstate.memory.address_prefixes['heap']:
            return

        raise_exception = True

        if cell.lookup['memory_mapped'] > self._vmstate.global_clock:
            if cell.lookup['old_memory_address'] != cell.address:
                # address changed
                anomaly = MemoryMapAnomaly(cell, self._vmstate.register_file.pc, self._vmstate.global_clock, False)
                
            elif cell.lookup['old_dimension'] != cell.dimension:
                # dimension changed
                anomaly = MemoryMapAnomaly(cell, self._vmstate.register_file.pc, self._vmstate.global_clock, False)
                
            elif cell.lookup['old_content'] != cell.content:
                # content changed (freed probably)
                anomaly = WARAnomaly(cell, self._vmstate.register_file.pc, self._vmstate.global_clock, False)
                anomaly.from_memory_map = True

            else:
                anomaly = MemoryMapAnomaly(cell, self._vmstate.register_file.pc, self._vmstate.global_clock, True)
                raise_exception = False

            # append only if the anomaly is not in the anomaly set.
            if anomaly not in self._vmstate.anomalies:
                self._vmstate.anomalies.append(anomaly)

                # stats
                self._vmstate.stats.anomaly_found()

                # check if not false-positive
                if not anomaly.is_false_positive:
                    # Stop test if user requires it
                    self._vmstate.handle_stop_request(anomaly)

            else:
                index = self._vmstate.anomalies.index(anomaly)
                self._vmstate.anomalies[index].is_false_positive &= anomaly.is_false_positive

            if raise_exception:

                # If dynamic checkpoint, then raise exception
                if self._vmstate.raise_memory_anomaly_exceptions:
                    anomaly.raise_exception()

                # If static checkpoint, signal it (so further analysis on subsequent instructions can be done)
                else:
                    self._vmstate.trigger_reset_and_restore = True


    def _check_for_memory_war_anomaly(self, cell):
        """
        Checks for memory write-after-read anomalies for a given cell.
        """

        # check for write after read hazards only if enabled.
        if not self._vmstate.do_data_anomaly_check:
            return None

        if cell.address_prefix not in self._vmstate.memory_trace_prefixes:
            return

        raise_exception = False

        # if write timestamp > current timestamp, possibly there is an error
        if cell.lookup['write_global_clock'] is not None and cell.lookup['write_global_clock'] > self._vmstate.global_clock:
            
            # false-positive
            if cell.lookup['old_content'] == cell.content:
                logging.info('{} <- {}'.format(cell.lookup['write_global_clock'], self._vmstate.global_clock))
                anomaly = WARAnomaly(cell, self._vmstate.register_file.pc, self._vmstate.global_clock, True)
                
            else:
                anomaly = WARAnomaly(cell, self._vmstate.register_file.pc, self._vmstate.global_clock, False)
                raise_exception = True

            # append only if the anomaly is not in the anomaly set.
            if anomaly not in self._vmstate.anomalies:
                self._vmstate.anomalies.append(anomaly)
                
                # stats
                self._vmstate.stats.anomaly_found()
                
                # check if not false-positive
                if not anomaly.is_false_positive:
                    # Stop test if user requires it
                    self._vmstate.handle_stop_request(anomaly)

            else:
                index = self._vmstate.anomalies.index(anomaly)
                self._vmstate.anomalies[index].is_false_positive &= anomaly.is_false_positive
            
            if raise_exception:
                
                # If dynamic checkpoint, then raise exception
                if self._vmstate.raise_memory_anomaly_exceptions:
                    anomaly.raise_exception()

                # If static checkpoint, signal it (so further analysis on subsequent instructions can be done)
                else:
                    self._vmstate.trigger_reset_and_restore = True


    def _get_cell(self, address, dimension, write_access):
        """
        Returns the cell present at the given address.
        Dimension is in bytes and is used to verify that the cell is consistent w.r.t. the requested type.
        If write_access is set, the cell dimension is adjusted to fit the given one, using the rebase method.
        """

        # dimension is already in bytes
        logging.debug('[{}] Getting cell at address {}{}{}.'.format(self.mem_type, self.address_prefix, hex(address), ' with write access' if write_access else ''))

        # If address not directly in memory, it can be contained inside a cell.
        # To obtain the address, rebase the container cell to make the wanted address directly accessible.
        if address not in self._memory:
            
            # get containing cell's address
            base_address = self._get_cell_base_address(address)
            
            if base_address is None:
                raise MemoryException('[{}] No memory cell starts at address {}{}'.format(self.mem_type, self.address_prefix, hex(address)))

            base_cell = self._memory[base_address]
            self._check_for_memory_map_anomaly(base_cell)

            # if cell not directly addressable, read must not fail but value must be None (in real life read will lead to a unattended value)
            if not write_access:
                cell = VirtualMemoryCell(address, self.address_prefix, dimension, None, False)
                cell.lookup = copy.deepcopy(base_cell.lookup)
                return cell
            
            # considered only in HEAP
            if base_cell.garbage:
                raise MemoryException('[{}] Unable to access address {}{}. Memory location is set as garbage'.format(self.mem_type, self.address_prefix, hex(address)))
            
            # calculate unwanted portion and rebase to separate from the wanted portion.
            new_dim = address - base_address
            self._rebase(base_address, new_dim)
            # now address is directly accessible in memory

        cell = self._memory[address]

        self._check_for_memory_map_anomaly(cell)

        # considered only in HEAP
        if cell.garbage:
            raise MemoryException('[{}] Unable to access address {}{}. Memory location is set as garbage'.format(self.mem_type, self.address_prefix, hex(address)))

        if cell.dimension != dimension:
            # if cell is not of the correct dimention, read must not fail but value must be None (in real life read will lead to a unattended value)
            if not write_access:

                # partial fix for in-memory accesses for structures
                # e.g. 32bit memcpy integer into a {16bit, 16bit}.
                # -> the problem is the memory representation, which does not allow that
                # future update: binary memory representation, instead of "contextual"
                if cell.dimension > dimension:
                    return cell

                return VirtualMemoryCell(address, self.address_prefix, dimension, None, False)

            # rebase to the wanted dimension
            self._rebase(address, dimension)
    
        return cell

    
    def read(self, address, dimension, dimension_in_bits = True, resolve_address = True):
        """
        Returns the content of a cell, given its address and dimension.
        If dimension is different from the one of the cell, it returns an invalid value (None)
        """

        if resolve_address:
            address = self.get_real_address(address)
            
        dimension = self.convert_dimension(dimension, dimension_in_bits)

        logging.debug('[{}] Reading {} bytes of memory at address {}{}.'.format(self.mem_type, dimension, self.address_prefix, hex(address)))

        cell = self._get_cell(address, dimension, False)

        self._check_for_memory_war_anomaly(cell)

        self._check_input_lookup(cell)

        cell.collect_memory_trace('read')

        return cell.content


    def get_cells_from_address(self, address, dimension, dimension_in_bits = True, resolve_address = True):
        """
        Returns the cells starting from a given address, s.t. the overall dimension is the given one.
        """

        if resolve_address:
            address = self.get_real_address(address)

        dimension = self.convert_dimension(dimension, dimension_in_bits)
        
        logging.debug('[{}] Getting {} bytes of memory from address {}{}.'.format(self.mem_type, dimension, self.address_prefix, hex(address)))

        cells = []

        while dimension > 0:
            if address not in self._memory:
                break

            cell = self._memory[address]
            self._check_for_memory_map_anomaly(cell)
            self._check_for_memory_war_anomaly(cell)

            dimension -= cell.dimension
            address += cell.dimension

            if dimension >= 0:
                cells.append(copy.deepcopy(cell))

        return cells


    def set_cells_from_address(self, address, cells, resolve_address = True):
        """
        Copies the content from a given list of cells starting from the given address.
        """

        if resolve_address:
            address = self.get_real_address(address)

        logging.debug('[{}] Setting memory from address {}{}.'.format(self.mem_type, self.address_prefix, hex(address)))

        for cell in cells:
            self.write(address, cell.dimension, cell.content, False, False)

            # preserve input lookup
            if self._vmstate.input_lookup_enabled:
                self.set_cell_input_lookup(address, copy.deepcopy(cell.get_input_lookup()), False)

            address += cell.dimension


    def set_cell_input_lookup(self, address, input_lookup_data, resolve_address = True):
        """
        Sets the input lookup information of cell in a given address.
        """

        # NB: emptiness of input lookup if input_lookup_data is [] is guaranteed by write operations
        # which removes completely the lookup infos.
        
        if len(input_lookup_data) == 0:
            return
            
        if resolve_address:
            address = self.get_real_address(address)

        logging.debug('[{}] Setting memory input lookup at address {}{}.'.format(self.mem_type, self.address_prefix, hex(address)))

        if address not in self._memory:
            raise MemoryException('[{}] No memory cell starts at address {}{}'.format(self.mem_type, self.address_prefix, hex(address)))

        # get cell
        cell = self._memory[address]

        # set input lookup
        if self._vmstate.input_lookup_enabled:
            cell.set_input_lookup(input_lookup_data)

    
    def get_cell_input_lookup(self, address, resolve_address = True):
        """
        Returns the input lookup information of cell in a given address.
        """

        if resolve_address:
            address = self.get_real_address(address)

        logging.debug('[{}] Getting memory input lookup at address {}{}.'.format(self.mem_type, self.address_prefix, hex(address)))

        if address not in self._memory:
            raise MemoryException('[{}] No memory cell starts at address {}{}'.format(self.mem_type, self.address_prefix, hex(address)))

        # get cell
        cell = self._memory[address]

        return cell.get_input_lookup()


    def write(self, address, dimension, content, dimension_in_bits = True, resolve_address = True):
        """
        Writes the given content into a cell, given its address.
        If dimension is different from the one of the cell, it gets rebased.
        """

        if resolve_address:
            address = self.get_real_address(address)

        dimension = self.convert_dimension(dimension, dimension_in_bits)

        logging.debug('[{}] Writing {} bytes of memory at address {}{} with content \'{}\'.'.format(self.mem_type, dimension, self.address_prefix, hex(address), content))
        
        cell = self._get_cell(address, dimension, True)
        old_content = copy.deepcopy(cell.content)

        content = copy.deepcopy(content)
        
        cell.content = content

        # set lookup information, but only if simulation started and only if required
        if self._vmstate.global_clock > 0:
            
            if self._vmstate.do_data_anomaly_check:
                cell.set_lookup(old_content, self._vmstate.register_file.pc, self._vmstate.global_clock)
            
            if self._vmstate.input_lookup_enabled:
                cell.set_input_lookup(tools.build_input_lookup_data(None, None))

            cell.collect_memory_trace('write')


    def diff(self, dump):
        """
        Returns the difference between the current state of the register file and the one saved inside a dump.
        """

        logging.debug('[{}] Comparing current state with a given dump.'.format(self.mem_type))

        if not isinstance(dump, self.__class__):
            raise MemoryException('Unable to compare {} dump: {} object expected, {} given.'.format(self.mem_type, self.mem_type, dump.__class__.__name__))

        diff = []

        if self._memory != dump._memory:
            mem_keys = list(self._memory.keys())
            dump_keys = list(dump._memory.keys())

            common_elements = [item for item in mem_keys if item in dump_keys]
            only_mem_keys = [item for item in mem_keys if item not in dump_keys]
            only_dump_keys = [item for item in dump_keys if item not in mem_keys]

            for i in common_elements:
                if self._memory[i] != dump._memory[i]:
                    address = '{}{}'.format(self.address_prefix, hex(dump._memory[i].address))
                    diff.append({'address': address, 'dump_value': dump._memory[i].content, 'current_value': self._memory[i].content})

            for i in only_mem_keys:
                address = '{}{}'.format(self.address_prefix, hex(self._memory[i].address))
                diff.append({'address': address, 'dump_value': None, 'current_value': self._memory[i].content})

            for i in only_dump_keys:
                address = '{}{}'.format(self.address_prefix, hex(dump._memory[i].address))
                diff.append({'address': address, 'dump_value': dump._memory[i].content, 'current_value': None})

        if self.top_address != dump.top_address:
            diff.append({'element': '{} config'.format(self.mem_type), 'element_name': 'top_address', 'dump_value': copy.deepcopy(dump.top_address), 'current_value': copy.deepcopy(self.top_address)})
        
        return diff
