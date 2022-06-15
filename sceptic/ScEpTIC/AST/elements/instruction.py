import logging

from ScEpTIC import tools

class Instruction:
    """
    Generic AST Instruction
    """

    _vmstate = None

    # number of clock tick to be increased by this instruction
    tick_count = 1

    def __init__(self):
        self.basic_block_id = None
        self.label = None
        self.preds = None
        self.metadata = None
        self._omit_target = False


    def __str__(self):
        retstr = ''

        if self.label is not None:
            retstr += '[{}]  '.format(self.label)

        if 'target' in self.__dict__ and not self._omit_target and self.target is not None:
            retstr += '{} = '.format(self.target)

        return retstr


    def save_in_target_register(self, value):
        """
        Saves a given value in the target register of the instruction, if present.
        """

        if self._omit_target or self.target is None:
            return

        # get target register name
        target = self.target.value

        self._vmstate.register_file.write(target, value)

        if self._vmstate.input_lookup_enabled:
            input_lookup_data = self.get_input_lookup()
            self._vmstate.register_file.set_input_lookup(target, input_lookup_data)

        logging.info('[{}] Saving result in {}'.format(self.instruction_type, target))


    def run(self):
        """
        Executes the operation and the target assignment.
        """

        value = self.get_val()
        self.save_in_target_register(value)

        # call run's callback
        self._vmstate.on_run(self.tick_count)


    def get_defs(self):
        """
        Returns a list of registers defined by this instruction. Usually its len will be 1 or 0.
        (used by register allocation)
        """

        if 'target' in self.__dict__.keys() and self.target is not None:
            return self.target.get_uses()

        return []


    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        return []


    def get_ignore(self):
        """
        Returns a list of register names to be ignored by register allocation.
        """

        return []


    def get_input_lookup(self):
        """
        Returns the input lookup data for the current operation
        """

        return tools.build_input_lookup_data(None, None)


    @property
    def instruction_type(self):
        """
        Returns the instruction type
        """

        return self.__class__.__name__


    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Skeleton.
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        pass
