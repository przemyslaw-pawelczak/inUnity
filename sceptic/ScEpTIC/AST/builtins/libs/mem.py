from ScEpTIC.AST.builtins.builtin import Builtin

"""
Heap-related library functions
"""

class malloc(Builtin):
    """
    Definition of the malloc() builtin
    """

    def get_val(self):
        address = self._vmstate.memory.heap.allocate(self.args[0], False)
        return address


class calloc(Builtin):
    """
    Definition of the calloc() builtin
    """

    def get_val(self):
        # two parameters: number of elements and element dimension
        num = self.args[0]
        dim = self.args[1]
        dimension = num * dim
        address = self._vmstate.memory.heap.allocate(dimension, False)

        # initialize to 0
        for i in range(0, num):
            
            addr = self._vmstate.memory.add_offset(address, i*dim, False)
            self._vmstate.memory.heap.write(addr, dim, 0, False)

        return address


class realloc(Builtin):
    """
    Definition of the realloc() builtin
    """

    def get_val(self):
        address = self._vmstate.memory.heap.reallocate(self.args[0], self.args[1], False)
        return address


class free(Builtin):
    """
    Definition of the free() builtin
    """

    def get_val(self):
        self._vmstate.memory.heap.deallocate(self.args[0])
        return 0


address_dimension = '{}{}'.format('i', Builtin._vmstate.memory.address_dimension)

# define malloc()
malloc.define_builtin('malloc', 'i32', address_dimension)

# define calloc()
calloc.define_builtin('calloc', 'i32, i32', address_dimension)

# define realloc()
realloc.define_builtin('realloc', '{}, i32'.format(address_dimension), address_dimension)

# define free()
free.define_builtin('free', 'i32', address_dimension)
