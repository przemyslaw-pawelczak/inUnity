from ScEpTIC.AST.builtins.builtin import Builtin
from ScEpTIC.AST.elements.value import Value

"""
LLVM library functions
"""

class memcpy(Builtin):
    """
    memcpy() builtin
    """

    def get_val(self):
        args = self.args
        destination = args[0]
        source = args[1]
        nbytes = args[2]

        cells = self._vmstate.memory.get_cells_from_address(source, nbytes, False)
        self._vmstate.memory.set_cells_from_address(destination, cells)


class memmove(Builtin):
    """
    memmove() builtin
    """

    def get_val(self):
        args = self.args
        destination = args[0]
        source = args[1]
        nbytes = args[2]

        cells = self._vmstate.memory.get_cells_from_address(source, nbytes, False)
        self._vmstate.memory.write(source, nbytes, None, False)
        self._vmstate.memory.set_cells_from_address(destination, cells)


class memset(Builtin):
    """
    memset() builtin
    """

    def get_val(self):
        args = self.args
        destination = args[0]
        nbytes = args[2]
        value = Value.convert_sint_to_bin(args[1], 8) * nbytes
        value = Value.convert_bin_to_sint(value)
        self._vmstate.memory.write(destination, nbytes, value, False)

"""
Definitions for the various versions of llvm.memcpy, llvm.memmove, llvm.memset
"""
address_dimension = '{}{}'.format('i', Builtin._vmstate.memory.address_dimension)

# in llvm 5, source destination len align isvolatile, in llvm7 align is missing.
# To support every version, it is defined only as if it has 3 arguments.
memcpy.define_builtin('llvm.memcpy.p0i8.p0i8.i16', '{}, {}, i16'.format(address_dimension, address_dimension), 'void')
memcpy.define_builtin('llvm.memcpy.p0i8.p0i8.i32', '{}, {}, i32'.format(address_dimension, address_dimension), 'void')
memcpy.define_builtin('llvm.memcpy.p0i8.p0i8.i64', '{}, {}, i64'.format(address_dimension, address_dimension), 'void')

memmove.define_builtin('llvm.memmove.p0i8.p0i8.i16', '{}, {}, i16'.format(address_dimension, address_dimension), 'void')
memmove.define_builtin('llvm.memmove.p0i8.p0i8.i32', '{}, {}, i32'.format(address_dimension, address_dimension), 'void')
memmove.define_builtin('llvm.memmove.p0i8.p0i8.i64', '{}, {}, i64'.format(address_dimension, address_dimension), 'void')

memset.define_builtin('llvm.memset.p0i8.i16', '{}, {}, i16'.format(address_dimension, address_dimension), 'void')
memset.define_builtin('llvm.memset.p0i8.i32', '{}, {}, i32'.format(address_dimension, address_dimension), 'void')
memset.define_builtin('llvm.memset.p0i8.i64', '{}, {}, i64'.format(address_dimension, address_dimension), 'void')
