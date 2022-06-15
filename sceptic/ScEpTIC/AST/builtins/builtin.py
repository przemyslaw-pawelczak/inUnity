import logging

from ScEpTIC.AST.elements.instruction import Instruction
from ScEpTIC.exceptions import NotImplementedException

from .linker import BuiltinLinker

class Builtin(Instruction):
    """
    Base object to be extended for builtin functions.
    HOW TO:
        1) create the new instruction to be executed
        2) Implement the get_val() method, returning the result of the instruction.
            Arguments can be obatined using the list self.args (index = index of arg), their
            values will be automatically resolved on runtime.
        3) Call the class method define_builtin on the class
        4) All the builtins will be loaded by calling link()

    Example:

    class LenTestInstruction(Builtin):
        def get_val(self):
            return len(self.args)

    LenTestInstruction.define_builtin('let_test_instruction', 'i32, i32, double, float, i8', 'i64')
    """

    # this value is used to increment the global clock.
    # Set this in the Builtin implementations equal to the number
    # of corresponding assemly instruction of the builtin.
    tick_count = 1
    builtins = []

    def __init__(self):
        super().__init__()

    @staticmethod
    def link():
        """
        Links the builtin Instructions creating a function.
        """

        for builtin in Builtin.builtins:
            logging.debug('[Builtin] Linking {}'.format(builtin['name']))
            BuiltinLinker(builtin['name'], builtin['arguments'], builtin['return_type'], builtin['instruction'])

    @classmethod
    def define_builtin(cls, name, arguments, return_type):
        """
        Define builtins, which will be loaded by the link() function.
        """

        element = {'instruction': cls, 'name': name, 'arguments': arguments, 'return_type': return_type}
        cls.builtins.append(element)

    def set_args(self, args):
        """
        Sets the arguments of the builtin.
        """

        self._args = args

    @property
    def args(self):
        """
        Returns the resolved value of the arguments.
        """

        args = []

        for arg in self._args:
            arg = arg.get_val()
            args.append(arg)

        return args

    def get_val(self):
        """
        NB: must be implemented by each builtin!
        """

        raise NotImplementedException('get_val() method for builtins is mandatory to be implemented!')

    def get_uses(self):
        """
        Returns the registers used by this instruction as a list of strings.
        (used by register allocation)
        """

        uses = []

        for arg in self._args:
            # support for var_args
            if isinstance(arg, list):
                for arg_i in arg:
                    uses = uses + arg_i.get_uses()
            else:
                uses = uses + arg.get_uses()

        return uses

    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        for arg in self._args:
            # support for var_args
            if isinstance(arg, list):
                for arg_i in arg:
                    arg_i.replace_reg_name(old_reg_name, new_reg_name)
            else:
                arg.replace_reg_name(old_reg_name, new_reg_name)

        if 'target' in self.__dict__ and self.target is not None:
            self.target.replace_reg_name(old_reg_name, new_reg_name)


    def __str__(self):
        retstr = super().__str__()
        retstr += '{}({})'.format(self.__class__.__name__, self._args)
        return retstr
