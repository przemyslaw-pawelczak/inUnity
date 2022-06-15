import collections

class GlobalVar:
    """
    AST node representing a global variable
    """

    # use a ordered dict to keep global variables in the same order as specified by the programmer.
    elements = collections.OrderedDict()

    def __init__(self, name, var_type, initial_val, is_constant, align, section, comdat, metadata):
        self.name = name

        self.is_constant = is_constant
        
        self.type = var_type
        self.initial_val = initial_val
        
        if align is None:
            align = 0

        self.align = int(align)
        
        self.section = section
        self.comdat = comdat
        
        self.metadata = metadata

        self.elements[self.name] = self


    def __str__(self):
        retval = 'global_var: '

        if self.section is not None:
            retval += '['+str(self.section)+'] '

        retval += '{} {}'.format(self.type, self.name)

        if self.initial_val is not None:
            retval += ' = {}'.format(self.initial_val)

        return retval
