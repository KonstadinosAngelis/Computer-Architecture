"""CPU functionality."""
import sys

class CPU:
    def __init__(self):
        self.ram = [0] * 256 #256 bytes of Memory
        self.reg = [0] * 8 #8 registers for quickly storing data
        self.pc = 0 #Progam counter for keeping a pointer of where we are in the program


    def load(self):
        address = 0

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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
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

    def ram_read(self, MAR): #Takes in a Memory Address Register (MAR) which is the position in the memory wanting to read
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): #Takes in the MAR like above function. Also takes in Memory Data Register (MDR) which is the data getting writting to the MAR
        self.ram[MAR] = MDR


    def run(self):
        running = True

        while running:
            ir = self.ram[self.pc]

            if ir == 0b00000001: #Halt
                running = False
                self.pc += 1

            elif ir == 0b10000010: #LDI
                reg_num = self.ram_read(self.pc + 1)
                val = self.ram_read(self.pc + 2)
                self.reg[reg_num] = val
                self.pc += 3

            elif ir == 0b01000111: #Print
                reg_num = self.ram_read(self.pc + 1)
                print(self.reg[reg_num])
                self.pc += 2

            else:
                print(f'Unknown Instruction {ir} at address {self.pc}')
                sys.exit(1)

newCPU = CPU()
newCPU.load()
newCPU.run()