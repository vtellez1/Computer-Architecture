"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        """
        # For now, we've just hardcoded a program:        
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        """
        #Bonus: check to make sure the user has put a command line argument where you expect,
        #  and print an error and exit if they didn't.
        if len(sys.argv) < 2:
                print("Error, need to specify program. Now exiting")
                sys.exit(1)

        # You will now want to use those command line arguments to open a file
        # Can look in sys.argv[1] for the name of the file to load.
        with open(sys.argv[1]) as f:
            # Read in its contents line by line
            for line in f:
                #Ignore everything after a #, since that's a comment
                string_val = line.split("#")[0].strip()
                #Be on the lookout for blank lines (ignore them)
                if string_val == '':
                    continue
                # Convert the binary strings to integer values to store in RAM. 
                # The built-in int() function can do that when you specify a 
                # number base as the second argument
                v = int(string_val, 2)
                #print(v)
                # And save appropriate data into RAM.
                self.ram[address] = v
                address += 1


    def ram_read(self, MAR):
        #Memory Address Register (MAR)        
        return self.ram[MAR]


    def ram_write(self, MDR, MAR):
        #Memory Address Register (MAR) and Memory Data Register (MDR)        
        self.ram[MAR] = MDR


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111


        running = True

        #Instruction Register (IR)
        IR = self.pc

        while running:
            instruction = self.ram_read(IR)

            if instruction == LDI:
                operand_a = self.ram_read(IR +1)
                operand_b = self.ram_read(IR +2)
                self.reg[operand_a] = operand_b
                IR += 3

            elif instruction == PRN:
                reg_num = self.ram_read(IR +1)
                print(self.reg[reg_num])
                IR += 2

            elif instruction == HLT:
                running = False
                sys.exit(0)

            else:
                print(f'Unknown instruction {instruction} at address {IR}')
                sys.exit(1)

