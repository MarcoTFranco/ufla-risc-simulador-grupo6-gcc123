# PARA RODAR POR ENQUANTO: python src/simulador.py

import sys

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

def main():
    print("Simulador UFLA-RISC - Em desenvolvimento")

if __name__ == "__main__":
    main()