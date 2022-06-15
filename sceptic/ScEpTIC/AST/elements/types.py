from ScEpTIC.exceptions import NotImplementedException


class BaseType:
    """
    AST node of LLVM Base Type
    NOTE: enum data type doesn't appear because it is directly resolved and converted in int by the llvm front-end.
    """

    def __init__(self, base_type, bits):
        self.type = base_type
        self.bits = int(bits)


    def __len__(self):
        return self.bits


    def __str__(self):
        return '{} {}bit'.format(self.type, self.bits)


    def __repr__(self):
        return 'BaseType({}, {})'.format(self.type, self.bits)


    def __eq__(self, other):
        if not isinstance(other, BaseType):
            return False

        return self.type == other.type and self.bits == other.bits


class Type:
    """
    AST node representing a LLVM generic type (Array, Vector, Pointer, Custom Type)
    """

    address_dimension = 0

    def __init__(self, is_pointer, pointer_level, is_array, array_composition, is_vector, vector_dimension, is_base_type, custom_type_name, is_ct_defined, custom_type_def, base_type):
        self.is_pointer = is_pointer
        self.pointer_level = int(pointer_level)

        self.is_array = is_array
        self._set_array_composition(array_composition)

        self.is_vector = is_vector
        self.vector_dimension = int(vector_dimension)

        self.is_base_type = is_base_type
        self.custom_type_name = custom_type_name

        self.is_ct_defined = is_ct_defined
        self.custom_type_def = custom_type_def

        self.base_type = base_type


    def _set_array_composition(self, array_composition):
        """
        Sets the array composition of the type.
        """

        self.array_composition = []
        
        for elem in array_composition:
            elem = int(elem)
            self.array_composition.append(elem)

        self.array_dimensions = len(self.array_composition)


    def _get_array_composition(self, element_dimension):
        """
        Returns the overall array cells number.
        """

        array_composition = self.array_composition.copy()
        array_composition.reverse()
        
        dim = element_dimension

        for i in array_composition:
            dim = [i, dim]

        return dim


    def get_memory_composition(self, flat_composition = False):
        """
        Returns the memory composition of the Type, which is a list [a, b]
        with a representing the number of elements and b representing the size of each element.
        b can be a list of memory composition in case the Type refers to a customtype.
        """

        element_dimension = 0

        # set dimension
        if self.is_pointer:
            element_dimension = self.address_dimension

        elif self.is_base_type:
            element_dimension = len(self.base_type)

        elif self.is_ct_defined:
            raise NotImplementedException('Type not supported')

        else:
            element_dimension = CustomType.elements[self.custom_type_name].get_memory_composition()

        # is is array, create proper composition
        if self.is_array:
            composition = self._get_array_composition(element_dimension)
    
        else:
            elements_number = 1
            
            if self.is_vector:
                elements_number = self.vector_dimension
            
            composition = [elements_number, element_dimension]
        
        if flat_composition:
            flat = []
            self.flat_composition(composition, flat)
            return flat

        return composition


    @staticmethod
    def flat_composition(composition, lst):
        """
        flatterns a memory composition, turning it into a single list of dimensions
        array: [2, 32] -> [32, 32]
        array of struct: [3, [[3, 8], [1, 32]]] -> [8, 8, 8, 32, 8, 8, 8, 32, 8, 8, 8, 32]
        """

        # scans the second part of a [,] which is the dimension
        if isinstance(composition, int):
            lst.append(composition)
            return

        repeat = composition[0]

        # is the repetition factor, so the subsequent one can be a dimension or a struct definition
        if isinstance(repeat, int):
            for _ in range(0, repeat):
                Type.flat_composition(composition[1], lst)

        # if repeat is not a list, is a struct definition (a list of [,])
        else:
            for sub_comp in composition:
                Type.flat_composition(sub_comp, lst)


    @classmethod
    def empty(cls):
        """
        Creates an empty type.
        """

        is_pointer = False
        pointer_level = 0

        is_array = False
        array_composition = []

        is_vector = False
        vector_dimension = 0

        is_base_type = True
        custom_type_name = None

        is_ct_defined = False
        custom_type_def = None

        base_type = None

        return cls(is_pointer, pointer_level, is_array, array_composition, is_vector, vector_dimension, is_base_type, custom_type_name, is_ct_defined, custom_type_def, base_type)


    def __len__(self):
        """
        Returns the size in bits of the type
        """

        len_multiplier = 1

        if self.is_vector:
            len_multiplier = self.vector_dimension

        if self.is_array:
            for i in self.array_composition:
                len_multiplier = len_multiplier * i

        if self.is_pointer:
            return len_multiplier * self.address_dimension

        elif self.is_base_type:
            return len_multiplier * len(self.base_type)
        
        elif self.is_ct_defined:
            tmp_len = 0
            for elem in self.custom_type_def:
                tmp_len = tmp_len + len(elem)

            return len_multiplier * tmp_len
        
        else:
            if self.custom_type_name not in CustomType.elements:
                raise ValueError('Custom type {} not found!'.format(self.custom_type_name))
            return len_multiplier * len(CustomType.elements[self.custom_type_name])


    def __str__(self):

        if self.is_base_type:
            retstr = str(self.base_type)+'*'*self.pointer_level
            
        elif self.is_ct_defined:
            retstr = 'CustomType: {'

            length = len(self.custom_type_def)-1

            for i in range(0, length+1):
                retstr += '{}'.format(self.custom_type_def[i])

                if i < length:
                    retstr += ', '

            retstr += '}'

        else:
            retstr = str(self.custom_type_name)

        if self.is_vector:
            retstr = '<{} x {}>'.format(self.vector_dimension, retstr)

        if self.is_array:
            retstr = '({})'.format(retstr)
            
            for i in self.array_composition:
                retstr = '{}[{}]'.format(retstr, i)

        return retstr


    def __repr__(self):
        return str(self)


class CustomType:
    """
    AST node representing a LLVM custom type
    """

    elements = {}

    def __init__(self, fullname, ct_type, name, type_composition):
        self.fullname = fullname
        self.type = ct_type
        self.name = name
        self._set_type_composition(type_composition)
        self.elements[self.fullname] = self


    def _set_type_composition(self, type_composition):
        """
        Sets the type composition of the custom type
        """

        self.type_composition = []

        for elem in type_composition:
            self.type_composition.append(elem)


    def __len__(self):
        """
        Returns the size in bits of the customtype
        """

        total_len = 0

        for elem in self.type_composition:
            total_len = total_len + len(elem)

        return total_len


    def __str__(self):
        retstr = ''

        length = len(self.type_composition)-1

        for i in range(0, length+1):
            retstr += '{}'.format(self.type_composition[i])

            if i < length:
                retstr += ', '

        # two {{ }} for printing single { }
        # middle {} to print retstr
        return '{}: {{{}}}'.format(self.fullname, retstr)


    def get_memory_composition(self):
        """
        Returns a list of lists, in which each element is a memory composition of the represented type.
        """

        elements = []
        for elem in self.type_composition:
            elements.append(elem.get_memory_composition())

        return elements
