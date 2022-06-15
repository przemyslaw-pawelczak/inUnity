import logging

from ScEpTIC import tools
from ScEpTIC.AST.elements.instruction import Instruction


class AllocaOperation(Instruction):
    """
    AST node of the LLVM Memory Instructions group - Alloca Instruction
    https://llvm.org/docs/LangRef.html#memoryops
    """

    def __init__(self, target, element_type, elements_number, align):
        self.target = target
        self.type = element_type
        self.elements_number = int(elements_number)
        self.align = int(align)

        super().__init__()

    def __str__(self):
        retstr = super().__str__()
        retstr += 'alloca {} x {}'.format(self.type, self.elements_number)
        return retstr

    def run(self):
        """
        Executes the operation and the target assignment.
        """

        target = self.target.value
        dimension = len(self.type) * self.elements_number

        address = self._vmstate.memory.stack.allocate(dimension, True, self.metadata)

        # use special write_address (datalayout omitted, value can't be stored in a physical register
        # since it is resolved and directly-placed by the compiler's backend)
        self._vmstate.register_file.write_address(target, address)
        
        # call run's callback
        self._vmstate.on_run(self.tick_count)

        logging.info('[{}] Allocating {} bits in stack at address {} ({}).'.format(self.instruction_type, dimension, address, target))
    

    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        # no register used
        return []


    def get_defs(self):
        """
        Returns a list of registers defined by this instruction.
        (used by register allocation)
        """

        # no register defined
        return []

    
    def get_ignore(self):
        """
        Returns a list of register names to be ignored by register allocation.
        For alloca operation it is the target register.
        """

        return self.target.get_uses()


    def get_input_lookup(self):
        """
        Returns the input lookup data for the current operation
        """

        return tools.build_input_lookup_data(None, None)


class LoadOperation(Instruction):
    """
    AST node of the LLVM Memory Instructions group - Load Instruction
    https://llvm.org/docs/LangRef.html#memoryops
    """

    def __init__(self, target, load_type, element, align, volatile):
        self.target = target
        self.type = load_type
        self.element = element
        self.align = int(align)
        self.is_volatile = volatile

        # In llvmir the arguments of a function are not stored in stack, but passed as virtual registers
        # or immediate values to the call().
        # To emulate the storing of the values onto the stack, save those values as address registers.
        # The register allocation step needs only to set self.is_arg_of_function_call to True, without touching
        # the target virtual register.
        # The arguments are loaded then onto the stack when the function needs them (the store is generated in the llvm ir already)
        self.is_arg_of_function_call = False

        super().__init__()


    def __str__(self):
        retstr = super().__str__()

        s_type = str(self.type)

        if self.element.type is not None:
            s_type = ''

        retstr += 'load {} {}{}'.format(s_type, self.element, ' [arg]' if self.is_arg_of_function_call else '')
        return retstr
    
    def run(self):
        """
        Executes the load operation and the target assignment.
        """

        value = self.get_val()
        
        # explained in __init__ comment
        if self.is_arg_of_function_call:
            target = self.target.value
            self._vmstate.register_file.write_address(target, value)
            
            if self._vmstate.input_lookup_enabled:
                input_lookup_data = self.get_input_lookup()
                self._vmstate.register_file.set_address_input_lookup(target, input_lookup_data)

        else:
            self.save_in_target_register(value)

        # call run's callback
        self._vmstate.on_run(self.tick_count)

        logging.info('[{}] Loading {} into {}.'.format(self.instruction_type, value, self.target.value))


    def get_val(self):
        """
        Executes the operation and the target assignment.
        """

        address = self.element.get_val()
        dimension = len(self.type)

        # read from memory
        value = self._vmstate.memory.read(address, dimension)

        return value


    def get_input_lookup(self):
        """
        Returns the input lookup data for the current operation
        """

        address = self.element.get_val()
        
        return self._vmstate.memory.get_cell_input_lookup(address)


    def get_load_address(self):
        """
        Returns the address to be loaded.
        """

        return self.element.get_val()
        

    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        self.element.replace_reg_name(old_reg_name, new_reg_name)
        self.target.replace_reg_name(old_reg_name, new_reg_name)
    
    
    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        return self.element.get_uses()

    def get_ignore(self):
        """
        Returns a list of register names to be ignored by register allocation.
        For load operation it is the target register, if the load operation is marked to be used
        as argument of a function call, since it will be loaded as a stack offset.
        """

        # if loads an argument of a function call, it is an address register (stack location)
        # so it must be ignored on register allocation.
        if self.is_arg_of_function_call:
            return self.target.get_uses()

        return []


class StoreOperation(Instruction):
    """
    AST node of the LLVM Memory Instructions group - Store Instruction
    https://llvm.org/docs/LangRef.html#memoryops
    """

    def __init__(self, target, value, align, volatile):
        self.target = target
        self.value = value
        self.align = int(align)
        self.is_volatile = volatile

        super().__init__()

        self._omit_target = True
    
    def __str__(self):
        retstr = super().__str__()

        retstr += 'store {} in {}'.format(self.value, self.target)
        return retstr

    def run(self):
        """
        Executes the operation and the target assignment.
        """

        address = self.target.get_val()
        dimension = len(self.value.type)
        content = self.value.get_val()
        
        # write into memory
        self._vmstate.memory.write(address, dimension, content)
        
        if self._vmstate.input_lookup_enabled:
            input_lookup_data = self.value.get_input_lookup()
            self._vmstate.memory.set_cell_input_lookup(address, input_lookup_data)
        
        # call run's callback
        self._vmstate.on_run(self.tick_count)

        logging.info('[{}] Saving {} into {}.'.format(self.instruction_type, content, self.target.value))

    
    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        return self.value.get_uses() + self.target.get_uses()


    def get_defs(self):
        """
        Returns a list of registers defined by this instruction.
        (used by register allocation)
        """

        return []


    def get_store_address(self):
        """
        Returns the address in which the value will be stored.
        """

        return self.target.get_val()


    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        self.value.replace_reg_name(old_reg_name, new_reg_name)
        self.target.replace_reg_name(old_reg_name, new_reg_name)


class GetElementPointerOperation(Instruction):
    """
    AST node of the LLVM Memory Instructions group - GetElementPointer Instruction
    https://llvm.org/docs/LangRef.html#memoryops
    """

    def __init__(self, target, element, base_type, indexes, inbounds):
        self.target = target
        self.element = element
        self.type = base_type
        # indexes is a list of Values with an additional inrage attribute (either True or False)
        self.indexes = indexes
        self.inbounds = inbounds

        super().__init__()


    def __str__(self):
        retstr = super().__str__()

        s_indexes = ''

        for i in self.indexes:
            s_indexes = '{}[{}]'.format(s_indexes, i)

        retstr += 'getelementpointer {} {}'.format(self.element, s_indexes)
        return retstr


    def get_val(self):
        """
        Returns the represented absolute address.
        """

        # get relative address to perform computation
        address = self.element.get_val()
        prefix, base_address = self._vmstate.memory._parse_absolute_address(address)
        
        # first index is the offset from the base_address (dimension of spacing = overall size of one element of composition self.type)
        # (is like "pointer" spacing)
        offset = len(self.type) * self.indexes[0].get_val()

        # C-like indexes starts from the second element of self.indexes
        indexes = self.indexes[1:]
        composition = self.type.get_memory_composition()

        # each index is an instance of Value
        for index in indexes:
            index = index.get_val()
            
            # compute only if index > 0
            if index > 0:
                sel_item = composition[0]

                flat = []

                # data-structure fixup for false-positive array detection
                if isinstance(composition[0], int) and composition[0] == 1 and isinstance(composition[1], list):
                    composition = composition[1]

                # array definition
                if isinstance(sel_item, int):
                    composition = composition[1]
                    self.type.flat_composition(composition, flat)
                    offset += index * sum(flat)

                # struct definition, select the proper element
                else:
                    # flat the composition until the selected index
                    composition = composition[1]
                    self.type.flat_composition(composition[0:index], flat)
                    composition = composition[index]
                    offset += sum(flat)

            else:
                if isinstance(composition[0], int):
                    composition = composition[1]
                else:
                    composition = composition[index]

        # offset is calculated in bits, address is in bytes
        if offset % 8 != 0:
            raise ValueError('Offset {} is not a multiple of a byte.'.format(offset))

        offset = offset // 8  # int division
        
        value = '{}{}'.format(prefix, hex(base_address + offset))

        logging.info('[{}] Address resolved to {}.'.format(self.instruction_type, value))

        return value

    
    def get_uses(self):
        """
        Returns a list containing the names of the registers used by this instruction.
        (used by register allocation)
        """

        uses = self.element.get_uses()
        for index in self.indexes:
            uses = uses + index.get_uses()

        return uses


    def replace_reg_name(self, old_reg_name, new_reg_name):
        """
        Replaces the name of a register used by the instruction with a new one.
        (used by register allocation)
        """

        self.element.replace_reg_name(old_reg_name, new_reg_name)

        for index in self.indexes:
            index.replace_reg_name(old_reg_name, new_reg_name)

        if self.target is not None:
            self.target.replace_reg_name(old_reg_name, new_reg_name)


    def get_input_lookup(self):
        """
        Returns the input lookup data for the current operation
        """

        # element is an address (or a reference to it), so does not have any input lookup info.
        # indexes may have input lookup infos
        lookup = tools.build_input_lookup_data(None, None)

        for index in self.indexes:
            lookup = tools.merge_input_lookup_data(lookup, index.get_input_lookup())

        return lookup
