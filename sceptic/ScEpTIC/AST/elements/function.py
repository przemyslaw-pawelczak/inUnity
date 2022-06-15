from ScEpTIC import tools
from ScEpTIC.exceptions import RuntimeException

from .instructions.memory_operations import AllocaOperation
from .instructions.other_operations import CallOperation
from .instructions.termination_instructions import BranchOperation

class Function:
    """
    AST node representing a function.
    Contains the function's definition and body.
    """

    elements = {}
    declarations = {}

    def __init__(self, name, return_type, arguments, attr_groups, metadata):
        self.name = name
        self.type = return_type

        # is a list of Types with additional attributes field.
        self.arguments = arguments

        self.attr_groups = attr_groups
        self.metadata = metadata
        self.body = None

        # dictionary that maps a label with the first instruction of the corresponding basic block
        self._instr_label_maps = {}
        self.declarations[self.name] = self

        # instance of the object in charge of performing register allocation over this function.
        # it is assigned by the register allocation and is used to perform pre and post processing.
        self.register_allocator = None
        
        # contains the names of the functions called by the current one. It is used by register
        # allocation, for finding the overall number of used registers, to emulate the saving of registers
        # before running a function. It also helps in finding the best possible allocation of registers
        # w.r.t. different functions.
        # NB: in self._calls recursion is not considered, since the number of registers to be saved
        # will be equal to the number of registers used by the function.
        self._calls = []

        self.is_input = False
        self.input_name = None
        self.is_builtin = False
        

    def __str__(self):
        retval = '{} {}()'.format(self.type, self.name, self.arguments)
        
        if self.body is not None:
            retval += '\n'+tools.fancy_list_to_str(self.body)

        return retval

    def __len__(self):
        return len(self.body)

    @property
    def first_basic_block_id(self):
        """
        Returns the id of the first basic block.
        If the function has some arguments, each argument is mapped starting from %0 to %(#args - 1)
        The first basic block label will be %(#args)
        """

        return '%{}'.format(len(self.arguments))


    def attach_body(self, body):
        """
        Sets the body of a function definition and creates the mapping between instruction id and labels.
        """

        self.elements[self.name] = self
        del self.declarations[self.name]
        self.body = body
        self.update_labels()
        self._populate_calls()
        self._adjust_useless_branch_ticks()

    def update_labels(self):
        """
        Updates the label-instruction mappings
        """

        self._instr_label_maps = {}
        for i in range(0, len(self.body)):
            instruction = self.body[i]

            if instruction.label is not None:
                self._instr_label_maps[instruction.label] = i


    def get_instruction_id(self, label):
        """
        Returns the instruction which has a given label.
        """

        if label not in self._instr_label_maps:
            raise RuntimeException('Unable to find label {} in function {}.'.format(label, self.name))

        return self._instr_label_maps[label]


    def get_ignore(self):
        """
        Returns a list of register names to be ignored by register allocation.
        For a function corresponds to the registers used to pass the parameters, which are from
        %0 to %(n-1) (n = number of arguments).
        """

        ignores = []
        for i in range(0, len(self.arguments)):
            ignores.append('%{}'.format(i))

        return ignores


    def _populate_calls(self):
        """
        Populates the self._call list.
        """

        self._calls = []

        for i in self.body:

            # if is a call operation, and is not a call to the same function append it to self._calls
            # recursion is not considered, since the obtained list is used to verify the maximun number of
            # register used by a function and a call to the same function won't change the number of registers
            # used by the function.
            if isinstance(i, CallOperation):
                name = i.name
                if name != self.name and name not in self._calls:
                    self._calls.append(name)

    def _remove_from_calls(self, name):
        """
        Removes a given function name from the self._call list
        """

        try:
            self._calls.remove(name)
        # element not in list
        except ValueError:
            pass


    def _adjust_useless_branch_ticks(self):
        """
        This method virtually removes the useless branch instructions, which are
        unconditional branches that jumps to the next instruction. Those branches are
        necessary to have a basic-block division, but in the real final machine code they will
        be removed. For such reason, the number of clock ticks to be increased by those branches is set to 0,
        so to run them but to do not interfere with the analysis. (This allows me to not remove them)
        """

        body_len = len(self.body)
        
        # nb: unconditional branches have condition = None

        for i in range(0, body_len):
            code = self.body[i]

            if isinstance(code, BranchOperation):
                # if is not an unconditional branch, skip
                if code.condition is not None:
                    continue

                # next instruction id
                next_instr_index = i+1

                # if a next instruction exists && if the branch jumps to the next instruction, set its tick to 0
                if next_instr_index < body_len and code.target_true == self.body[next_instr_index].label:
                    code.tick_count = 0

    def adjust_alloca_ticks(self):
        """
        This method sets all the ticks for alloca operations equal to 0, except for the last one.
        Alloca operations are merged together during datalayout into a single ebp increment.
        The last alloca is the one with tick = 1 for skipping the entire alloca section when running in
        intermittent execution (otherwise multiple alloca operations might be run, but the result would be wrong)
        """

        body_len = len(self.body)
        last_alloca_id = -1

        args = len(self.arguments)

        # scan the code for alloca operations
        for i in range(0, body_len):
            code = self.body[i]

            if not isinstance(code, AllocaOperation):
                continue

            last_alloca_id = i
            code.tick_count = 0

            var_metadata = code.metadata.retrieve() if code.metadata is not None else None

            if var_metadata is None or 'variable_name' not in var_metadata:
                metadata_append = ''
            else:
                metadata_append = ' "{}"'.format(var_metadata['variable_name'])

            metadata_prepend = 'function argument' if i < args else 'local variable'

            code.metadata = '{}{}'.format(metadata_prepend, metadata_append)
                            
        if last_alloca_id >= 0:
            self.body[last_alloca_id].tick_count = 1
