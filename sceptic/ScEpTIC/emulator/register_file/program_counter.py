from ScEpTIC.exceptions import RegisterFileException

class ProgramCounter:
    """
    Program Counter.
    This emulator doesn't assign a direct address to each instruction, so
    the PC is composed by the function name and the instruction number inside the function.
    function_name is used to get the correct context.
    The program counter can be seen as the address of function_name plus instruction_number (which is just an offset from function_name's address).
    Since the actual program is not converted into machine code, the llvmir doesn't have a proper address and this representation is needed.
    """
    _vmstate = None


    def __init__(self, function_name, instruction_number):
        self._pc_tracking = []
        self.update(function_name, instruction_number)


    def __eq__(self, other):
        if not isinstance(other, ProgramCounter):
            return False

        # Ignore builtins implementations to verify if a program counter is equal to another.
        # In such case, it does not matter if it is at instruction #1 of builtin and the other at #2.
        # The thing that matters is the _pc_tracking: if the call is the same, the pc are equals.
        if self.function_name not in self._vmstate.functions or self._vmstate.functions[self.function_name].is_builtin:
            return self._pc_tracking == other._pc_tracking

        return self.function_name == other.function_name and self.instruction_number == other.instruction_number


    def __hash__(self):
        return hash((self.function_name, self.instruction_number))


    def __str__(self):
        return '{} -> #{}'.format(self.function_name, self.instruction_number)


    def __repr__(self):
        return 'ProgramCounter({}, {})'.format(self.function_name, self.instruction_number)


    def update(self, function_name, instruction_number):
        """
        Updates the function_name and instruction_number with the provided values.
        """

        self.function_name = function_name
        self.instruction_number = instruction_number


    def increment_pc(self):
        """
        Increments the instruction_number.
        """

        self.instruction_number = self.instruction_number + 1


    def save(self):
        """
        Returns a dump of the program counter.
        """

        return {'function_name': self.function_name, 'instruction_number': self.instruction_number}


    def restore(self, saved_pc):
        """
        Restores the program counter from a previous dump.
        """

        if 'function_name' not in saved_pc or 'instruction_number' not in saved_pc:
            raise RegisterFileException('Invalid ProgramCounter dump!')

        self.update(saved_pc['function_name'], saved_pc['instruction_number'])


    def resolve(self):
        """
        Returns the call trace of the program counter.
        """

        retval = ''
        ident = ''

        for pc in self._pc_tracking + [self.save()]:
            ident += ' '*4

            function_name = pc['function_name']
            instruction_number = pc['instruction_number']

            llvm_pc = '{} -> #{}'.format(function_name, instruction_number)

            function = self._vmstate.functions[pc['function_name']]
            metadata = function.body[pc['instruction_number']].metadata

            if metadata is not None:
                try:
                    pc_metadata = metadata.retrieve()
                    pc_metadata = ' ({})'.format(metadata.fancy_format(pc_metadata))

                except Exception:
                    pc_metadata = ' (No metadata found!)'

            else:
                pc_metadata = ' (Builtin function)' if function.is_builtin else ' (No metadata found!)'

            retval += '{}{}{}\n'.format(ident, llvm_pc, pc_metadata)

        return retval


    def pc_tree(self):
        """
        Returns the program counter with its call tree
        """

        pc_tree = ''

        for pc in self._pc_tracking:
            pc_tree = '{}{}#{},'.format(pc_tree, pc['function_name'], pc['instruction_number'])

        instruction_number = self.instruction_number

        if self.function_name not in self._vmstate.functions or self._vmstate.functions[self.function_name].is_builtin:
            instruction_number = 0

        return '{}{}#{}'.format(pc_tree, self.function_name, instruction_number)
