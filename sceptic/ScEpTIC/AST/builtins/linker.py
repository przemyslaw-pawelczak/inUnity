import logging

from ScEpTIC.AST.elements.function import Function
from ScEpTIC.AST.elements.instructions.memory_operations import AllocaOperation, LoadOperation, StoreOperation
from ScEpTIC.AST.elements.instructions.termination_instructions import ReturnOperation
from ScEpTIC.AST.elements.value import Value
from ScEpTIC.llvmir_parser.sections_parser import global_vars

class BuiltinLinker:
    """
    This class generates the code of a builtin function.
    Builtin functions are implementation of library functions (e.g. sqrt, pow) that performs some
    architecture-dependent operations, which doesn't modify the control flow nor the memory (SRAM, NVM).

    In case control-flow modification or memory accesses are needed, it is better to directly create some C code
    for them and include it in the final code to be analyzed.

    Builtins are just used to not include in the final code library operations, and should not be used to
    emulate memory accesses, global variables accesses, direct-memory writes and other major operations,
    which can be easily implemented in the program code.

    An example of a builtins are mathematical functions and printing functions.

    The core of a builtin is an extension of the Instruction operation. This is needed to be able to analyze the code.


    Normally LLVM will consider the arguments to be from virtual register %0 to %(#args - 1)
    and the %(#args) is the ID of the first basic block. Since the builtins should not have labels and control-flow operations,
    it is omitted.

        Arguments are passed from %0 to %(len(args) - 1)
        Arguments addresses in stack are stored from %(len(args)) to %(len(args)*2 - 1)
        Arguments values are loaded from %(len(args) * 2) to %(len(args) * 3 - 1)
        Return value will be on %(len(args) * 3)

    """

    prefix = None
    
    def __init__(self, name, arguments, return_type, instruction):
        self.name = "{}{}".format(self.prefix if self.prefix is not None else '', name)
        
        # link only if a declaration exists, which means that the function is used inside the program.
        if self.name not in Function.declarations:
            return None
            
        self.arguments = self._parse_arguments(arguments)
        self.return_type = global_vars.parse_type(return_type, True, True)
        self.body = []
        self._attach_instruction(instruction)
        
        logging.info('[BuiltinLinker] Linking {} into {}'.format(instruction.__name__, self.name))
        
        self.is_input = instruction.is_input if hasattr(instruction, 'is_input') else False
        self.input_name = instruction.input_name if self.is_input else None

        self._link()


    @staticmethod
    def _parse_arguments(arguments):
        """
        Parses the argument string and returns a list of types
        """
        
        # no arguments
        if len(arguments) == 0:
            return []

        arguments = arguments.split(',')
        args = []
        for i in arguments:
            # remove initial spaces
            if i[0] == ' ':
                i = i[1:]

            arg = global_vars.parse_type(i, True, True)
            args.append(arg)

        return args


    def _link(self):
        """
        Creates the function, attach the body and maps it into function_definitions.
        """

        f = Function(self.name, self.return_type, self.arguments, None, None)
        f.attach_body(self.body)
        f.is_input = self.is_input
        f.input_name = self.input_name
        f.is_builtin = True


    def _attach_instruction(self, instruction):
        """
        Attach the actual ad-hoc code.
        """

        self._arguments_init()

        # set target register
        target = self._get_return_register()
        instruction = instruction()
        instruction.target = target

        args = self._get_arguments()
        instruction.set_args(args)

        self.body.append(instruction)
        
        self._generate_return()


    def _get_argument_type(self, argument_id):
        """
        Returns the type of a given argument
        """

        return self.arguments[argument_id]


    def _get_argument_register_address(self, argument_id):
        """
        Returns the register which contains the address in which the argument will be, as a Value.
        """

        reg_id = '%{}'.format(len(self.arguments) + argument_id)
        reg_type = self._get_argument_type(argument_id)

        return Value('virtual_reg', reg_id, reg_type)


    def _get_argument_register(self, argument_id):
        """
        Returns the register containing the value of the given argument, as a Value.
        """

        reg_id = '%{}'.format((len(self.arguments) * 2) + argument_id)
        reg_type = self._get_argument_type(argument_id)

        return Value('virtual_reg', reg_id, reg_type)


    def _get_passed_argument_register(self, argument_id):
        """
        Returns the virtual register in which the passed argument is.
        """

        reg_id = '%{}'.format(argument_id)
        reg_type = self._get_argument_type(argument_id)

        return Value('virtual_reg', reg_id, reg_type)


    def _generate_save_argument_in_stack(self, argument_id):
        """
        Generates the operations needed to save the given argument onto the stack.
        """

        # allocate space on stack
        target = self._get_argument_register_address(argument_id)
        elements_number = 1
        align = 0
        alloca = AllocaOperation(target, target.type, elements_number, align)
        self.body.append(alloca)

        # save passed argument onto the stack
        value = self._get_passed_argument_register(argument_id)
        align = 0
        volatile = False
        store = StoreOperation(target, value, align, volatile)
        self.body.append(store)


    def _save_arguments(self):
        """
        Saves the arguments onto the stack.
        """

        for i in range(0, len(self.arguments)):
            self._generate_save_argument_in_stack(i)


    def _generate_load_argument_from_stack(self, argument_id):
        """
        Generates the load operation which loads from stack into a register the given argument.
        """

        target = self._get_argument_register(argument_id)
        load_type = self._get_argument_type(argument_id)
        element = self._get_argument_register_address(argument_id)
        align = 0
        volatile = False
        load = LoadOperation(target, load_type, element, align, volatile)
        self.body.append(load)


    def _load_arguments(self):
        """
        Loads the arguments onto the stack.
        """

        for i in range(0, len(self.arguments)):
            self._generate_load_argument_from_stack(i)
    

    def _arguments_init(self):
        """
        Saves onto the stack the arguments and loads them into the corresponding register.
        """

        self._save_arguments()
        self._load_arguments()
    

    def _get_arguments(self):
        """
        Returns the arguments (as Value virtual_reg) of the builtin.
        This must be used by the actual builtin-code.
        """

        args = []
        for i in range(0, len(self.arguments)):
            arg = self._get_argument_register(i)
            args.append(arg)

        return args


    def _get_return_register(self):
        """
        Returns the register in which the return value will be contained.
        """

        reg_id = '%{}'.format(len(self.arguments) * 3)

        return Value('virtual_reg', reg_id, self.return_type)


    def _generate_return(self):
        """
        Generates the return instruction needed at the end of the builtin.
        """

        value = self._get_return_register()
        ret = ReturnOperation(value)
        self.body.append(ret)
