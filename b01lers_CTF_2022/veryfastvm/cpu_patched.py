import sys
import os
import random
import struct
X13 = 1024*1024
X14 = 10
X15 = 2000
X16 = 55 
class Instruction:
    op = None
    imm = 0
    dst_reg = None
    src_reg = None
    dsp = None
    jmp_imm = None
    memory_addr = 0
    consume_time = 0
    def __init__(self, tstr):
        def X06(tt):
            if tt.startswith("0x"):
                try:
                    v = int(tt, 16)
                except ValueError:
                    assert False
            else:
                try:
                    v = int(tt)
                except ValueError:
                    assert False
            assert v>=0
            assert v<pow(2,32)
            return v
        def X17_jmp_imm(tt): # -1000 < tt < 1000
            try:
                v = int(tt)
            except ValueError:
                assert False
            assert v>-1000
            assert v<1000
            return v
        def X07(tt): # r0 <= tt <= r9
            assert len(tt) == 2
            assert tt[0] == "r"
            try:
                v = int(tt[1])
            except ValueError:
                assert False
            assert v>=0
            assert v<X14
            return v
        def X17_memory(tt):
            try:
                v = int(tt)
            except ValueError:
                assert False
            assert v>=0
            assert v<X13
            return v
        assert len(tstr)<100
        sstr = tstr.split()
        assert len(sstr)>=1
        assert len(sstr)<=4
        if len(sstr) == 1:
            t_op = sstr[0]
            assert t_op in ["halt", "time", "magic", "reset"]
            self.op = t_op
        elif len(sstr) == 2:
            t_op, t_1 = sstr
            assert t_op in ["jmp", "jmpz"]
            self.op = t_op
            if self.op == "jmp":
                self.jmp_imm = X17_jmp_imm(t_1)
            elif self.op == "jmpz":
                self.jmp_imm = X17_jmp_imm(t_1)
            else:
                assert False
        elif len(sstr) == 3:
            t_op, t_1, t_2 = sstr
            assert t_op in ["mov", "movc", "jmpg", "add", "sub", "mul", "and", "or", "xor"]
            self.op = t_op
            if self.op == "mov":
                self.dst_reg = X07(t_1)
                self.src_reg = X07(t_2)
            elif self.op in ["add", "sub", "mul", "and", "or", "xor"]:
                self.dst_reg = X07(t_1)
                self.src_reg = X07(t_2)
            elif self.op == "movc":
                self.dst_reg = X07(t_1)
                self.imm = X06(t_2)
            elif self.op == "jmpg":
                self.jmp_imm = X17_jmp_imm(t_2)
                self.dst_reg = X07(t_1)
            else:
                assert False
        elif len(sstr) == 4:
            t_op, t_1, t_2, t_3 = sstr
            assert t_op in ["movfrom", "movto"]
            self.op = t_op
            if self.op == "movfrom":
                self.dst_reg = X07(t_1)
                self.memory_addr = X17_memory(t_2)
                self.dsp = X07(t_3)
            elif self.op == "movto":
                self.dst_reg = X07(t_1)
                self.memory_addr = X17_memory(t_2)
                self.dsp = X07(t_3)
            else:
                assert False
        else:
            assert False
    def pprint(self):
        tstr = "%s %s %s %s %s %s" %            (self.op, 
            "None" if self.dst_reg==None else "r%d"%self.dst_reg,
            "None" if self.src_reg==None else "r%d"%self.src_reg,
            hex(self.imm), "None" if self.jmp_imm==None else self.jmp_imm, self.memory_addr)
        return tstr
class Cpu:
    Instruction_Counter = 0 
    instructions = None
    Registers = None 
    memory = None # 1024 * 1024
    consume_time = 0
    cache = None
    Reset_Counter = 0
    Random_Numbers = None
    def __init__(self):
        self.instructions = []
        self.cache = {}
        self.Random_Numbers = (random.randint(1,4200000000), random.randint(1,4200000000) , random.randint(1,4200000000), random.randint(1,4200000000))
        self.reset()
    def reset(self):
        self.Instruction_Counter = 0
        self.Registers = [0 for r in range(X14)]
        self.memory = [0 for _ in range(X13)]
        self.consume_time = 0
        for k in self.cache.keys():
            self.cache[k] = 0
        self.Reset_Counter += 1
    def load_instructions(self, tt):
        for line in tt.split("\n"):
            if "#" in line:
                line = line.split("#")[0]
            line = line.strip()
            if not line:
                continue
            self.instructions.append(Instruction(line))
            assert len(self.instructions) <= X16
    def run(self, debug=0):
        ins = self.instructions[0]
        for i,v in enumerate(self.Random_Numbers):
            self.memory[i] = v
        while (self.Instruction_Counter>=0 and self.Instruction_Counter<len(self.instructions) and self.Reset_Counter<4 and self.consume_time<20000):
            ins = self.instructions[self.Instruction_Counter]
            self.execute(ins)
    def execute(self, ins):
        self.consume_time += 1
        if ins.op == "movc":
            self.Registers[ins.dst_reg] = ins.imm
            self.Instruction_Counter += 1
        elif ins.op == "magic":
            if self.Reset_Counter == 2: # cpu reset counter == 2
                if tuple(self.Registers[0:4]) == self.Random_Numbers:
                    with open("flag.txt", "rb") as fp:
                        cc = fp.read()
                    cc = cc.strip()
                    cc = cc.ljust(len(self.Registers)*4, b"\x00")
                    for i in range(len(self.Registers)):
                        self.Registers[i] = struct.unpack("<I", cc[i*4:(i+1)*4])[0]
            self.Instruction_Counter += 1
        elif ins.op == "reset":
            self.reset()
        elif ins.op == "halt":
            self.Instruction_Counter = len(self.instructions)
        elif ins.op == "time":
            self.Registers[0] = self.consume_time
            self.Instruction_Counter += 1
        elif ins.op == "jmp":
            nt = self.Instruction_Counter + ins.jmp_imm
            assert nt >=0 
            assert nt < len(self.instructions)
            self.Instruction_Counter = nt
        elif ins.op == "jmpz":
            if self.Registers[0] == 0:
                nt = self.Instruction_Counter + ins.jmp_imm
                assert nt >=0 
                assert nt < len(self.instructions)
                self.Instruction_Counter = nt
            else:
                self.Instruction_Counter += 1
        elif ins.op == "jmpg":
            if self.Registers[0] > self.Registers[ins.dst_reg]:
                nt = self.Instruction_Counter + ins.jmp_imm
                assert nt >=0 
                assert nt < len(self.instructions)
                self.Instruction_Counter = nt
            else:
                self.Instruction_Counter += 1
        elif ins.op == "mov":
            self.Registers[ins.dst_reg] = self.Registers[ins.src_reg]
            self.Instruction_Counter += 1
        elif ins.op == "sub":
            v = self.Registers[ins.dst_reg] - self.Registers[ins.src_reg]
            self.Registers[ins.dst_reg] = (v & 0xffffffff)
            self.Instruction_Counter += 1
        elif ins.op == "add":
            v = self.Registers[ins.dst_reg] + self.Registers[ins.src_reg]
            self.Registers[ins.dst_reg] = (v & 0xffffffff)
            self.Instruction_Counter += 1
        elif ins.op == "mul":
            v = self.Registers[ins.dst_reg] * self.Registers[ins.src_reg]
            self.Registers[ins.dst_reg] = (v & 0xffffffff)
            self.Instruction_Counter += 1
        elif ins.op == "and":
            v = self.Registers[ins.dst_reg] & self.Registers[ins.src_reg]
            self.Registers[ins.dst_reg] = (v & 0xffffffff)
            self.Instruction_Counter += 1
        elif ins.op == "or":
            v = self.Registers[ins.dst_reg] | self.Registers[ins.src_reg]
            self.Registers[ins.dst_reg] = (v & 0xffffffff)
            self.Instruction_Counter += 1
        elif ins.op == "xor":
            v = self.Registers[ins.dst_reg] ^ self.Registers[ins.src_reg]
            self.Registers[ins.dst_reg] = (v & 0xffffffff)
            self.Instruction_Counter += 1
        elif ins.op == "movfrom":
            X09 = ins.memory_addr + self.Registers[ins.dsp]
            X09 = X09 % len(self.memory)
            if X09 in self.cache:
                v = self.cache[X09]
                v = (v & 0xffffffff)
                self.Registers[ins.dst_reg] = v
                self.Instruction_Counter += 1
            else:
                v = self.memory[X09]
                self.cache[X09] = v
                self.execute(ins)
        elif ins.op == "movto":
            X09 = ins.memory_addr + self.Registers[ins.dsp]
            X09 = X09 % len(self.memory)
            if X09 in self.cache:
                del self.cache[X09]
            v = (self.Registers[ins.dst_reg] & 0xffffffff)
            self.memory[X09] = v
            self.Instruction_Counter += 1
        else:
            assert False
        return 
    def pprint(self, debug=0):
        tstr = ""
        tstr += "%d> "%self.Instruction_Counter # instruction counter
        tstr += "[%d] "%self.consume_time
        tstrl = []
        for i,r in enumerate(self.Registers): # dump registers
            tstrl.append("r%d=%d"%(i,r))
        tstr += ",".join(tstrl)
        if debug>1:
            tstr += "\nM->"
            vv = []
            for i,v in enumerate(self.memory):
                if v!=0:
                    vv.append("%d:%d"%(i,v))
            tstr += ",".join(vv)
            tstr += "\nC->"
            tstr += repr(self.cache)
        return tstr
def main():
    print("Welcome to a very fast VM!")
    print("Give me your instructions.")
    print("To terminate, send 3 consecutive empty lines.")
    instructions = ""
    X18 = 0
    while True:
        line = input()
        if not line.strip():
            X18 += 1
        else:
            X18 = 0
        instructions += line + "\n"
        if X18 >= 3 or len(instructions) > X15:
            break
    print(instructions)
    print(X18)
    c = Cpu()
    print("Parsing...")
    c.load_instructions(instructions)
    print("Running...")
    c.run()
    print("Done!")
    print("Registers: " + repr(c.Registers))
    print("Goodbye.")
if __name__ == "__main__":
    sys.exit(main())
