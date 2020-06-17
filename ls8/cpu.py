"""CPU functionality."""
import sys

program_file = "ls8\examples\mult.ls8"

class CPU:
    def __init__(self):
        self.ram = [0] * 256 #256 bytes of Memory
        self.reg = [0] * 8 #8 registers for quickly storing data
        self.pc = 0 #Progam counter for keeping a pointer of where we are in the program

    def load(self, program):
        with open(program) as p:
            address = 0

            for line in p:

                line = line.split("#")

                try:
                    v = line[0].strip()
                except ValueError:
                    continue
                
                if len(v) > 0:
                    self.ram[address] = int(v,2)

                    address += 1

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, MAR): #Takes in a Memory Address Register (MAR) which is the position in the memory wanting to read
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): #Takes in the MAR like above function. Also takes in Memory Data Register (MDR) which is the data getting writting to the MAR
        self.ram[MAR] = MDR

    def run(self):
        running = True

        while running:
            ir = self.ram[self.pc]
            if ir == 0b00000001: #HALT
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
            
            elif ir == 0b10100010: #Mul
                num1 = self.reg[self.ram_read(self.pc + 1)]
                num2 = self.reg[self.ram_read(self.pc + 2)]

                result = num1 * num2

                self.reg[self.ram_read(self.pc + 1)] = result

                self.pc += 3

            else:
                print(f'Unknown Instruction {ir} at address {self.pc}')
                sys.exit(1)

newCPU = CPU()
newCPU.load(program_file)
newCPU.run()