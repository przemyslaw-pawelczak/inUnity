import copy
import logging

from ScEpTIC import tools
from ScEpTIC.emulator.intermittent_executor.anomalies import InputPolicyAnomaly
from ScEpTIC.emulator.io.input import InputManager
from ScEpTIC.exceptions import RegisterNotFoundException, RegisterFileException

from .program_counter import ProgramCounter
from .register import Register


class RegisterFile:
    """
    Register File. It contains registers of the architecture.
    The _reg_stack dictionary is used to save/restore registers or addresses on function call/return.
    This will preserve the correctness of the program, witout having to:
        - Perform register allocation
        - Perform datalayout calculation if register allocation is done
    """

    _vmstate = None

    def __init__(self):
        # contains the registers.
        self._registers = {}

        # lookup table for input information
        self._input_lookup = {}

        # register stack used to manage function call and returns.
        # NB: this is not the sobstitution of the stack, so if spills happens, they are inserted inside the stack (and not in reg_stack).
        # this is just used to permit virtual registers and omit data layout.
        self._reg_stack = []
        
        # Program Counter
        self.pc = ProgramCounter(None, 0)
        # Stack Base Pointer
        self.ebp = 0
        # Stack Pointer (ESP) is top_address attribute of the Stack class.
        
        # keeps track of the previous basic block, to support phi operation.
        self.last_basic_block = '%0'

        logging.info('{} initialized.'.format(self.reg_type))


    def __str__(self):
        retval = 'PC: {}\nEBP: {}\n\n'.format(self.pc, hex(self.ebp))
        for reg in self._registers:
            retval += str(self._registers[reg])+"\n"

        return retval
    

    def __len__(self):
        return len(self._registers)


    def __eq__(self, other):
        if not isinstance(other, RegisterFile):
            return False

        return self._registers == other._registers and self._reg_stack == other._reg_stack and self._input_lookup == other._input_lookup and self.pc == other.pc and self.ebp == other.ebp


    @property
    def reg_type(self):
        """
        Returns register file type
        """

        return self.__class__.__name__


    def _create_register(self, register_name):
        """
        Creates a register with name register_name
        """

        logging.debug('[{}] Creating register {}'.format(self.reg_type, register_name))
        self._registers[register_name] = Register(register_name)


    def _get_register(self, register_name, operation):
        """
        Returns a register.
        Operation is passed to support virtual registers: in that case, on write a register can be created.
        """
        if register_name not in self._registers:
            raise RegisterNotFoundException('[{}] Register {} not found!'.format(self.reg_type, register_name))

        return self._registers[register_name]

    
    def get_input_lookup(self, register_name):
        """
        Returns the input lookup information for a given register.
        """

        if register_name not in self._input_lookup:
            return tools.build_input_lookup_data(None, None)

        return self._input_lookup[register_name]

    
    def set_input_lookup(self, register_name, input_lookup_data):
        """
        Sets the input lookup information for a given register.
        """

        # NB: emptiness of input lookup if input_lookup_data is [] is guaranteed by write operations
        # which removes completely the lookup infos.
        
        if len(input_lookup_data) > 0:
            self._input_lookup[register_name] = input_lookup_data


    def set_address_input_lookup(self, register_name, input_lookup_data):
        """
        Sets the input lookup information for a given address register.
        """

        self.set_input_lookup(register_name, input_lookup_data)


    def _check_input_lookup(self, register_name):
        if not self._vmstate.input_lookup_enabled:
            return None

        checkpoint_clock = self._vmstate.checkpoint_clock

        # get lookup info from memory cell
        input_lookup_data = self.get_input_lookup(register_name)

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
                    access_pc = self.pc
                    anomaly = InputPolicyAnomaly(checkpoint_pc, checkpoint_clock, access_pc, clock_id, input_name, measured_consistency, consistency)
                    
                    if anomaly not in self._vmstate.anomalies:
                        self._vmstate.anomalies.append(anomaly)
                        
                        # stats
                        self._vmstate.stats.anomaly_found()

                        # Stop test if user requires it
                        self._vmstate.handle_stop_request(anomaly)


    def read(self, register_name):
        """
        Return the value of a register given its name.
        """

        logging.debug('[{}] Reading register {}'.format(self.reg_type, register_name))

        register = self._get_register(register_name, 'read')

        self._check_input_lookup(register_name)

        return register.value


    def write(self, register_name, register_value):
        """
        Set the value of a register given its name.
        """

        logging.debug('[{}] Writing register {} with value {}'.format(self.reg_type, register_name, register_value))

        register = self._get_register(register_name, 'write')
        register.value = copy.deepcopy(register_value)

        # remove input lookup on write.
        if register_name in self._input_lookup:
            del self._input_lookup[register_name]


    def write_address(self, register_name, address):
        """
        Set the value of an address register.
        Address are considered only as values returned by alloca operations.
        There are different behaviours depending on physical/virtual register file.
        On physical register file, register allocation is performed.
        Alloca operations just make space on stack and their value is known compile-time.
        This means that the virtual register wouldn't be mapped to a real one, since the stack
        offset is found and directly placed on the load/store operation that uses this portion of memory.
        Also, multiple alloca operations will be mapped to a single increment of the stack.
        (This is done in data layout)
        NB: this is to do not have register's spill due to not doing data layout. In a "real" machine code, those spills won't be there
        """

        self.write(register_name, address)

        # remove input lookup on write.
        if register_name in self._input_lookup:
            del self._input_lookup[register_name]


    def read_address(self, register_name):
        """
        Returns the value of an address register.
        """

        return self.read(register_name)


    def dump(self):
        """
        Returns a dump of the register file.
        """

        logging.debug('Creating dump of {}.'.format(self.reg_type))

        return copy.deepcopy(self)


    def restore(self, dump):
        """
        Restores a dump of the register file.
        """
        logging.debug('Restoring dump of {}.'.format(self.reg_type))

        if not isinstance(dump, self.__class__):
            raise RegisterFileException('Unable to restore {} dump: {} object expected, {} given.'.format(self.reg_type, self.reg_type, dump.__class__.__name__))

        self._registers = copy.deepcopy(dump._registers)
        self._input_lookup = copy.deepcopy(dump._input_lookup)
        self._reg_stack = copy.deepcopy(dump._reg_stack)
        
        self.pc = copy.deepcopy(dump.pc)
        self.ebp = copy.deepcopy(dump.ebp)
        self.last_basic_block = copy.deepcopy(dump.last_basic_block)


    def compare_with_dump(self, dump):
        """
        Returns if the status of register file is the same of a given dump.
        """

        return self == dump


    def get_visual_dump(self):
        """
        Returns a string representing the memory
        """

        dump = 'PC: '+str(self.pc)+'\n'

        for i in sorted(self._registers.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 0):
            dump += str(self._registers[i])+"\n"

        return dump


    def reset(self, main):
        """
        Performs the reset of the register_file (after a cpu reset).
        """

        self._registers = {}
        self._reg_stack = []
        self._input_lookup = {}
        self.pc = ProgramCounter(main, 0)
        self.ebp = 0
        self.last_basic_block = '%0'


    def diff(self, dump):
        """
        Returns the difference between the current state of the register file and the one saved inside a dump.
        """

        logging.debug('[{}] Comparing current state with a given dump.'.format(self.reg_type))

        if not isinstance(dump, self.__class__):
            raise RegisterFileException('Unable to compare {} dump: {} object expected, {} given.'.format(self.reg_type, self.reg_type, dump.__class__.__name__))

        diff = []

        if self._registers != dump._registers:
            reg_keys = list(self._registers.keys())
            dump_keys = list(dump._registers.keys())

            common_elements = [item for item in reg_keys if item in dump_keys]
            only_reg_keys = [item for item in reg_keys if item not in dump_keys]
            only_dump_keys = [item for item in dump_keys if item not in reg_keys]

            for i in common_elements:
                if self._registers[i] != dump._registers[i]:
                    diff.append({'register': i, 'dump_value': copy.deepcopy(dump._registers[i].value), 'current_value': copy.deepcopy(self._registers[i].value)})

            for i in only_reg_keys:
                diff.append({'register': i, 'dump_value': None, 'current_value': copy.deepcopy(self._registers[i].value)})

            for i in only_dump_keys:
                diff.append({'register': i, 'dump_value': copy.deepcopy(dump._registers[i].value), 'current_value': None})

        if self._reg_stack != dump._reg_stack:
            diff.append({'element': 'register_stack', 'dump_value': copy.deepcopy(dump._reg_stack), 'current_value': copy.deepcopy(self._reg_stack)})

        if self.ebp != dump.ebp:
            diff.append({'register': 'EBP', 'dump_value': copy.deepcopy(dump.ebp), 'current_value': copy.deepcopy(self.ebp)})
        
        if self.pc != dump.pc:
            diff.append({'register': 'PC', 'dump_value': copy.deepcopy(dump.pc), 'current_value': copy.deepcopy(self.pc)})

        if self.last_basic_block != dump.last_basic_block:
            diff.append({'register': 'LAST_BASC_BLOCK', 'dump_value': copy.deepcopy(dump.last_basic_block), 'current_value': copy.deepcopy(self.last_basic_block)})

        return diff
