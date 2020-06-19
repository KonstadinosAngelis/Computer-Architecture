"""CPU functionality."""
import sys

program_file = "ls8\examples\sctest.ls8"

class CPU:
    def __init__(self):
        self.ram = [0] * 256 #256 bytes of Memory
        self.reg = [0] * 8 #8 registers for quickly storing data
        self.flags = [0] * 8
        self.pc = 0 #Progam counter for keeping a pointer of where we are in the program
        self.sp = 7
        self.reg[self.sp] = 0xf4
        self.branch_table = {
            0b00000001: self.halt,
            0b10000010: self.ldi,
            0b01000111: self.print,
            0b10100010: self.multiply,
            0b10100000: self.add,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010000: self.call,
            0b00010001: self.ret,
            0b01010100: self.jpm,
            0b10100111: self.comp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
        }

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

    def ram_read(self, MAR): #Takes in a Memory Address Register (MAR) which is the position in the memory wanting to read
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): #Takes in the MAR like above function. Also takes in Memory Data Register (MDR) which is the data getting writting to the MAR
        self.ram[MAR] = MDR

    def halt(self):
        self.pc += 1
        sys.exit()

    def ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        val = self.ram_read(self.pc + 2)
        self.reg[reg_num] = val
        self.pc += 3

    def print(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])
        self.pc += 2

    def add(self):
        num1 = self.reg[self.ram_read(self.pc + 1)]
        num2 = self.reg[self.ram_read(self.pc + 2)]
        
        self.reg[self.ram_read(self.pc + 1)] = (num1 + num2)

        self.pc += 3

    def multiply(self):
        num1 = self.reg[self.ram_read(self.pc + 1)]
        num2 = self.reg[self.ram_read(self.pc + 2)]

        result = num1 * num2

        self.reg[self.ram_read(self.pc + 1)] = result

        self.pc += 3
    
    def push(self, push_num = None):
        self.reg[self.sp] -= 1
        
        if push_num:
            val = push_num
        else:
            reg_num = self.ram_read(self.pc + 1)
            val = self.reg[reg_num]

        stack_pos = self.reg[self.sp]

        self.ram_write(stack_pos, val)

        self.pc += 2

    def pop(self):
        pop_val = self.ram_read(self.reg[self.sp])

        self.ram_write(self.reg[self.sp], 0)

        self.reg[self.sp] += 1

        reg_num = self.ram_read(self.pc + 1)
        self.reg[reg_num] = pop_val

        self.pc += 2

    def call(self):
        reg_val = self.reg[self.ram_read(self.pc + 1)]
        self.push(self.pc)
        self.pc = reg_val

    def ret(self):
        
        pop_val = self.ram_read(self.reg[self.sp])

        self.ram_write(self.reg[self.sp], 0)
        self.reg[self.sp] += 1
        
        self.pc = pop_val + 2

    def jpm(self):
        jump_pos = self.reg[self.ram_read(self.pc + 1)]
        self.pc = jump_pos

    def comp(self):
        val1 = self.reg[self.ram_read(self.pc + 1)]
        val2 = self.reg[self.ram_read(self.pc + 2)]
        
        if val1 == val2:
            self.flags[self.ram_read(self.pc + 1)] = 'E'
        if val1 < val2:
            self.flags[self.ram_read(self.pc + 1)] = 'L'
        if val1 > val2:
            self.flags[self.ram_read(self.pc + 1)] = 'G'

        self.pc += 3

    def jeq(self):
        comp_val = self.flags[0]
        if comp_val == 'E':
            jump_val = self.reg[self.ram_read(self.pc + 1)]
            self.pc = jump_val
        else:
            self.pc += 2

    def jne(self):
        comp_val = self.flags[0]
        if comp_val != 'E':
            jump_val = self.reg[self.ram_read(self.pc + 1)]
            self.pc = jump_val
        else:
            self.pc += 2
        
    def run(self):
        running = True
        while running:
            ir = self.ram[self.pc]

            if ir in self.branch_table:
                self.branch_table[ir]()

            else:
                print(f'Unknown Instruction {ir} at address {self.pc}')
                sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

newCPU = CPU()
newCPU.load(program_file)
newCPU.run()
