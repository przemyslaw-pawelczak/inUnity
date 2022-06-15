from ScEpTIC.exceptions import RegAllocException

class RegisterPool:
    """
    Pool of registers used by register allocation to get available registers.
    """

    def __init__(self, regs_number, reg_prefix):
        # list of registers state: True -> free; False -> in use
        self.registers = [True for x in range(regs_number)]
        self.regs_number = regs_number
        self.reg_prefix = reg_prefix


    def get_reg(self):
        """
        Returns a free register. If no register is available, it raises a RegAllocException
        The returned register is marked as busy.
        """

        for reg_id in range(0, self.regs_number):
            if self.registers[reg_id]:
                # set the register to in use
                self.registers[reg_id] = False
                return '{}{}'.format(self.reg_prefix, reg_id)

        raise RegAllocException('No register available for register allocation!')


    def _get_id_from_reg_name(self, reg_name):
        """
        Returns the id of a register, given its name.
        """

        if reg_name is None:
            return None
            
        reg_name = reg_name.replace(self.reg_prefix, '')
        return int(reg_name)


    def free_reg(self, reg_name):
        """
        Marks a given register as free.
        """

        reg_id = self._get_id_from_reg_name(reg_name)
        self.registers[reg_id] = True
