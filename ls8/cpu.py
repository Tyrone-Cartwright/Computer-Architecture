"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0] * 256  # instructions
        self.register = [0] * 8  # 8 register
        self.pc = 0  # program counter

        self.running = True

    def ram_read(self, MAR):
        return self.memory[MAR]

    def ram_write(self, MDR, MAR):
        self.memory[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # if len(sys.argv) != 2:
        #     print(f'usage: {sys.argv[0]} [file]')
        #     sys.exit(1)

        # try:
        #     with open(sys.argv[1]) as f:
        #         for line in f:
        #             # find first part of instruction
        #             number = line.split('#')[0]
        #             # replace all \n with empty space
        #             number = number.replace('\n', '')
        #             # remove any empty space
        #             number = number.strip()

        #             # forgot about the bland lines, convert binary to int and store in memory
        #             if number is not '':
        #                 number = int(number, 2)
        #                 # add to the memory
        #                 self.memory[address] = number
        #                 address += 1

        # except FileNotFoundError:
        #     print(f'{sys.argv[0]}: File not found')
        #     sys.exit(2)

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.memory[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        ir = self.memory[self.pc]
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        while self.running:

            def find(x):
                return {
                    'HLT': self.op_hlt(),
                    'LDI': self.op_ldi(operand_a, operand_b),
                    'PRN': self.op_prn(operand_a)
                }.get(x, 'HLT')

            find(ir)

    def op_ldi(self, operand_a, operand_b):
        self.register[operand_a] = operand_b

    def op_hlt(self):
        self.running = False

    def op_prn(self, operand_a):
        print(self.register[operand_a])
