import random

from ScEpTIC.AST.builtins.builtin import Builtin
from ScEpTIC.AST.elements.value import Value

"""
some stdio.h library functions
"""

class printf(Builtin):
    """
    Definition of the printf() builtin
    """

    stdout_enabled = True

    def get_val(self):
        address = self.args[0]
        gst = self._vmstate.memory.gst._get_gst_from_address(address)

        format_str = "{}".format(gst.read_string_from_address(address))
        args = tuple(self.args[1])

        if self.stdout_enabled:
            print("[PRINTF]: {}".format(format_str % args))

        return 0


class debug_print(Builtin):
    """
    Definition of the debug_print() builtin
    Note: you can use debug_print() inside your code and will print all the arguments that it receives.
    """

    def get_val(self):
        print('[Debug Print]: {}'.format(self.args))

        return 0


class memcmp(Builtin):
    """
    Definition of the memcmp() builtin
    """

    def get_val(self):
        buffer_1_addr = self.args[0]
        buffer_2_addr = self.args[1]

        # element number of i8 -> bytes
        buffer_length = self.args[2]

        buffer_1 = self._vmstate.memory.get_cells_from_address(buffer_1_addr, buffer_length, False)
        buffer_2 = self._vmstate.memory.get_cells_from_address(buffer_2_addr, buffer_length, False)

        for i in range(0, len(buffer_1)):
            val_1 = buffer_1[i].content
            if isinstance(val_1, str):
                val_1 = ord(val_1)

            val_2 = buffer_2[i].content
            if isinstance(val_2, str):
                val_2 = ord(val_2)

            # compensate for memory representation
            if val_1 < 0:
                val_1 = Value.convert_sint_to_uint(val_1, buffer_1[i].dimension*8)

            if val_2 < 0:
                val_2 = Value.convert_sint_to_uint(val_2, buffer_2[i].dimension*8)

            if val_1 != val_2:
                return val_1 - val_2

        return 0


class randombuiltin(Builtin):
    """
    Definition of the rand() builtin
    """

    def get_val(self):
        RAND_MAX = 32767
        return random.randint(0, RAND_MAX)


class srandombuiltin(Builtin):
    """
    Definition of the srand() builtin
    """

    def get_val(self):
        random.seed(int(self.args[0]))


class exitbuiltin(Builtin):
    """
    Definition of the exit() builtin
    """

    def get_val(self):
        # set program to its end
        self._vmstate.register_file.pc.update(self._vmstate._main_function_name, self._vmstate._main_function_len)

        # set main return value to the one passed to exit
        self._vmstate.main_return_value = self.args[0]

# definition for printf()
printf.define_builtin('printf', 'i32, ...', 'void')

# custom print
debug_print.define_builtin('debug_print', 'i32', 'void')

# definition for memcmp() and strncmp()
memcmp.define_builtin('memcmp', 'i8, i8, i64', 'i32')
memcmp.define_builtin('strncmp', 'i8, i8, i64', 'i32')

# random functions
randombuiltin.define_builtin('rand', '', 'i32')
srandombuiltin.define_builtin('srand', 'i32', 'void')

# definition for exit()
exitbuiltin.define_builtin('exit', 'i32', 'void')
