import math

from ScEpTIC.AST.builtins.builtin import Builtin

"""
math.h most used library functions
"""

class ceil(Builtin):
    """
    Definition of the ceil() builtin
    """

    def get_val(self):
        return math.ceil(self.args[0])

class floor(Builtin):
    """
    Definition of the floor() builtin
    """

    def get_val(self):
        return math.floor(self.args[0])

class fabs(Builtin):
    """
    Definition of the fabs() builtin
    """

    def get_val(self):
        return math.fabs(self.args[0])

class fmod(Builtin):
    """
    Definition of the fmod() builtin
    """

    def get_val(self):
        return math.fmod(self.args[0], self.args[1])

class sqrt(Builtin):
    """
    Definition of the sqrt() builtin
    """

    def get_val(self):
        return math.sqrt(self.args[0])

class pow(Builtin):
    """
    Definition of the pow() builtin
    """

    def get_val(self):
        return math.pow(self.args[0], self.args[1])

class exp(Builtin):
    """
    definition of the exp() builtin
    """

    def get_val(self):
        return math.exp(self.args[0])

class log(Builtin):
    """
    definition of the log() builtin
    """

    def get_val(self):
        return math.log(self.args[0])

class log10(Builtin):
    """
    definition of the log10() builtin
    """

    def get_val(self):
        return math.log10(self.args[0])

class acos(Builtin):
    """
    definition of the acos() builtin
    """

    def get_val(self):
        return math.acos(self.args[0])

class asin(Builtin):
    """
    Definition of the asin() builtin
    """

    def get_val(self):
        return math.asin(self.args[0])

class atan(Builtin):
    """
    Definition of the atan() builtin
    """

    def get_val(self):
        return math.atan(self.args[0])

class atan2(Builtin):
    """
    Definition of the atan2() builtin
    """

    def get_val(self):
        return math.atan2(self.args[0], self.args[1])

class cos(Builtin):
    """
    Definition of the cos() builtin
    """

    def get_val(self):
        return math.cos(self.args[0])

class cosh(Builtin):
    """
    Definition of the cosh() builtin
    """

    def get_val(self):
        return math.cosh(self.args[0])

class sin(Builtin):
    """
    Definition of the sin() builtin
    """

    def get_val(self):
        return math.sin(self.args[0])

class sinh(Builtin):
    """
    Definition of the sinh() builtin
    """

    def get_val(self):
        return math.sinh(self.args[0])

class tan(Builtin):
    """
    Definition of the tan() builtin
    """

    def get_val(self):
        return math.tan(self.args[0])

class tanh(Builtin):
    """
    Definition of the tanh() builtin
    """

    def get_val(self):
        return math.tanh(self.args[0])


ceil.define_builtin('ceil', 'double', 'double')
floor.define_builtin('floor', 'double', 'double')
fabs.define_builtin('fabs', 'double', 'double')
fmod.define_builtin('fmod', 'double, double', 'double')
sqrt.define_builtin('sqrt', 'double', 'double')
pow.define_builtin('pow', 'double, double', 'double')
exp.define_builtin('exp', 'double', 'double')
log.define_builtin('log', 'double', 'double')
log10.define_builtin('log10', 'double', 'double')

acos.define_builtin('acos', 'double', 'double')
asin.define_builtin('asin', 'double', 'double')
atan.define_builtin('atan', 'double', 'double')
atan2.define_builtin('atan2', 'double, double', 'double')
cos.define_builtin('cos', 'double', 'double')
cosh.define_builtin('cosh', 'double', 'double')
sin.define_builtin('sin', 'double', 'double')
sinh.define_builtin('sinh', 'double', 'double')
tan.define_builtin('tan', 'double', 'double')
tanh.define_builtin('tanh', 'double', 'double')

sin.define_builtin('llvm.sin.f64', 'double', 'double')
cos.define_builtin('llvm.cos.f64', 'double', 'double')
