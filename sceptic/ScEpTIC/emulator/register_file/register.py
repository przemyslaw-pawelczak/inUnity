class Register:
    """
    Register object. It has just a name and a value.
    This emulator is not interested in the actual type nor the data representation.
    """

    def __init__(self, name):
        self.name = name
        self.value = None

    def __repr__(self):
        return 'Register({}, {})'.format(self.name, self.value)


    def __str__(self):
        return '{}: {}'.format(self.name, self.value)


    def __eq__(self, other):
        if not isinstance(other, Register):
            return False

        return self.name == other.name and self.value == other.value

    @staticmethod
    def direct(name, value):
        """
        Initializes a register, sets its value, and returns it.
        """

        reg = Register(name)
        reg.value = value
        return reg
