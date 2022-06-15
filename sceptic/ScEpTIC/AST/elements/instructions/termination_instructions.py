import logging

from ScEpTIC.AST.elements.instruction import Instruction

class ReturnOperation(Instruction):
    """
    AST node of the LLVM Termination Instructions group  -  Return Instruction
    https://llvm.org/docs/LangRef.html#terminators
    """

    # esp = ebp
    # pop ebp
    # ebp = ebp_pop
    # pop pc
    # pc = pc_pop
    # store retval
    tick_count = 6

    def __init__(self, value):
        self.value = value
        self.update_pc = True

        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'return {}'.format(self.value)
        return retstr


    def run(self):
        """
        Retrieves the value of the return operation and calls the return's callback.
        """

        value = self.value.get_val()
        input_lookup = self.value.get_input_lookup()

        logging.info('[{}] Returning value {}.'.format(self.instruction_type, value))
        
        self._vmstate.on_function_return(value, input_lookup, self.tick_count, self.update_pc)

    
    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        return self.value.get_uses()

    
    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        self.value.replace_reg_name(old_reg_name, new_reg_name)


class BranchOperation(Instruction):
    """
    AST node of the LLVM Termination Instructions group  -  Branch Instruction
    https://llvm.org/docs/LangRef.html#terminators
    """

    # if condition is None: target = target_true directly
    def __init__(self, condition, target_true, target_false):
        self.condition = condition
        self.target_true = target_true
        self.target_false = target_false

        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'branch {} {} {}{}'.format(self.condition, self.target_true, self.target_false, ' [Useless]' if self.tick_count == 0 else '')
        return retstr


    def run(self):
        """
        Executes the branch operation.
        """

        # if condition is none, is an unconditional branch
        if self.condition is None:
            target = self.target_true
        else:
            # evaluates the condition
            value = self.condition.get_val()
            if int(value) == 1:
                target = self.target_true
            else:
                target = self.target_false

        # performs callback call
        self._vmstate.on_branch(target, self.basic_block_id, self.tick_count)
        
        logging.info('[{}] Branching to {} (condition is {}).'.format(self.instruction_type, target, True if self.condition is None else value))


    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        if self.condition is not None:
            return self.condition.get_uses()

        return []

    
    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        if self.condition is not None:
            self.condition.replace_reg_name(old_reg_name, new_reg_name)


class SwitchOperation(Instruction):
    """
    AST node of the LLVM Termination Instructions group  -  Switch Instruction
    https://llvm.org/docs/LangRef.html#terminators
    """

    def __init__(self, element, default_label, switch_pairs):
        self.element = element
        self.default_label = default_label
        # switch_pairs is a list of Value with additional label attribute
        self.switch_pairs = switch_pairs

        super().__init__()


    def __str__(self):
        retstr = super().__str__()
        retstr += 'switch {}; default: {}; {}'.format(self.element, self.default_label, self.switch_pairs)
        return retstr


    def run(self):
        """
        Executes the switch operation.
        """

        target_value = self.element.get_val()
        label = None

        for value in self.switch_pairs:
            val = value.get_val()

            # if value found, set label
            if val == target_value:
                label = value.label
                break

        # if label not set, use default_label
        if label is None:
            label = self.default_label

        # performs callback call
        self._vmstate.on_branch(label, self.basic_block_id, self.tick_count)

        logging.info('[{}] Branching to {}.'.format(self.instruction_type, label))

    
    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        return self.element.get_uses()

    
    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """
        self.element.replace_reg_name(old_reg_name, new_reg_name)
