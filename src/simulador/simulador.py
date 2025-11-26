# PARA RODAR POR ENQUANTO: python src/simulador.py binarios.txt

import sys

MASK32 = 0xFFFFFFFF
def to_u32(x): 
    return x & MASK32

def to_s32(x):
    x = x & MASK32
    return x if x < 0x80000000 else x - 0x100000000


# Esqueleto da classe que representa o estado da CPU
class CPUState:
    def __init__(self):
        self.regs = [0] * 32
        self.PC = 0
        self.IR = 0
        self.neg = 0
        self.zero = 0
        self.carry = 0
        self.overflow = 0

# Esqueleto da classe principal do simulador
class Simulator:
    def __init__(self):
        self.mem = [0] * 65536
        self.cpu = CPUState()
        self.cycle_counter = 0
        self.halted = False

    def load_program_text(self, path):
        addr = 0
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                parts = line.split()
                if parts[0].lower() == 'address':
                    if len(parts) < 2:
                        raise ValueError("Diretiva address sem argumento")
                    addr = int(parts[1], 2)
                    continue
                binstr = ''.join(ch for ch in line if ch in '01')
                if len(binstr) != 32:
                    raise ValueError(
                        f"Expected 32-bit binary line, got: {line}")
                instr = int(binstr, 2)
                if addr < 0 or addr >= len(self.mem):
                    raise IndexError("Address out of memory range")
                self.mem[addr] = instr
                addr += 1

    def execute_one_instruction(self):
        instr_addr = self.cpu.PC
        instr_word = self.mem[instr_addr]
        self.cpu.IR = instr_word
        self.cpu.PC = to_u32(self.cpu.PC + 1)

        if instr_word == 0xFFFFFFFF:
            print("[HALT fetched] Parando execução.")
            self.halted = True
            return

        print(
            f"[WARN] Opcode não implementado para instrução: {instr_word:032b}")
        self.halted = True  # Para temporariamente para evitar loop infinito

    def run(self, max_cycles=1000):
        while not self.halted:
            if self.cycle_counter > max_cycles:
                break
            self.execute_one_instruction()
        print("\\nExecução finalizada.")



def main():
    if len(sys.argv) < 2:
        print("Uso: python src/simulator.py binarios.txt")
        return
    path = sys.argv[1]
    sim = Simulator()
    sim.load_program_text(path)
    sim.run()


if_name_ == "_main_":
    main()