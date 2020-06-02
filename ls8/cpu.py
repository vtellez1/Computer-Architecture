"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        #R7 is the sp
        self.reg[self.sp] = 0xF4
        self.fl = [0] * 8

        
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[ADD] = self.handle_ADD

        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE


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

    def handle_LDI(self):
        operand_a = self.ram_read(self.pc +1)
        operand_b = self.ram_read(self.pc +2)
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_PRN(self):
        reg_num = self.ram_read(self.pc +1)
        print(self.reg[reg_num])
        self.pc += 2

    def handle_HLT(self):
        running = False
        sys.exit(0)

    def handle_MUL(self):
        op_a = self.ram_read(self.pc + 1)
        a = self.reg[op_a]
        op_b = self.ram_read(self.pc +2)
        b = self.reg[op_b]
        ab_product = a * b
        self.reg[op_a] = ab_product
        self.pc +=3
    
    def handle_PUSH(self):
        self.reg[self.sp] -= 1

        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]

        address = self.reg[self.sp]
        self.ram[address] = value

        self.pc += 2

    def handle_POP(self):
        address = self.reg[self.sp]
        value = self.ram[address]

        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = value

        self.reg[self.sp] += 1
       
        self.pc += 2

    def handle_CALL(self):
        return_adr = self.pc + 2

        # Push it on the stack
        self.reg[self.sp] -= 1
        top_of_stack_addr = self.reg[self.sp]
        self.ram[top_of_stack_addr] = return_adr

        # Set the PC to the subroutine addr
        reg_num = self.ram[self.pc + 1]
        subroutine_addr = self.reg[reg_num]

        self.pc = subroutine_addr

    def handle_RET(self):
        # Pop the retunr adr off stack
        top_of_stack_addr = self.reg[self.sp]
        return_addr = self.ram[top_of_stack_addr]
        self.reg[self.sp] += 1

        #store it in the PC
        self.pc = return_addr

    def handle_ADD(self):
        op_a = self.ram_read(self.pc + 1)
        a = self.reg[op_a]
        op_b = self.ram_read(self.pc +2)
        b = self.reg[op_b]
        ab_product = a + b
        self.reg[op_a] = ab_product
        self.pc +=3
    
    def handle_CMP(self):
        op_a = self.ram_read(self.pc + 1)
        a = self.reg[op_a]
        op_b = self.ram_read(self.pc +2)
        b = self.reg[op_b]

        # 00000LGE
        #Compare the values in two registers.
        # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
        if a == b:
            self.fl[7] = 1
            self.fl[6] = 0
            self.fl[5] = 0

        # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
        elif a < b:
            self.fl[5] = 1
            self.fl[7] = 0
            self.fl[6] = 0

        # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.        
        elif a > b:
            self.fl[6] = 1
            self.fl[5] = 0
            self.fl[7] = 0

        self.pc +=3        

    def handle_JMP(self):
        #Jump to the address stored in the given register.
        register = self.ram_read(self.pc + 1)
        # Set the PC to the address stored in the given register.
        self.pc = self.reg[register]

    def handle_JEQ(self):
        # If E (self.fl[7]) flag is set (true), jump to the address stored in the given register.
        if self.fl[7] == 1:
            self.handle_JMP()
        else:
            self.pc +=2

    def handle_JNE(self):
        # if E (slef.fl[7]) flag is clear (false, 0), jump to the address stored in the given register.
        if self.fl[7] == 0:
            self.handle_JMP()
        else:
            self.pc +=2


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

        running = True
        while running:           
            instruction = self.ram_read(self.pc)
            if instruction:
                self.branchtable[instruction]()
            else:
                print(f'Unknown instruction {instruction} at address {self.pc}')
                sys.exit(1)

 

