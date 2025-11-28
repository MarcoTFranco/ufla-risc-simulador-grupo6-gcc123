"""
opcodes.py - Tabela de Opcodes e Constantes

Define todos os opcodes do UFLA-RISC e constantes relacionadas.
"""

# Mapeamento de mnemônicos para opcodes
OPCODES = {
    # Instruções básicas (22 do enunciado)
    "add": 0x01,
    "sub": 0x02,
    "zeros": 0x03,
    "xor": 0x04,
    "or": 0x05,
    "passnota": 0x06,
    "and": 0x07,
    "asl": 0x08,
    "asr": 0x09,
    "lsl": 0x0A,
    "lsr": 0x0B,
    "passa": 0x0C,
    "lch": 0x0E,
    "lcl": 0x0F,
    "load": 0x10,
    "store": 0x11,
    "jal": 0x12,
    "jr": 0x13,
    "beq": 0x14,
    "bne": 0x15,
    "j": 0x16,

    # Instruções adicionais (8+ compartilhadas)
    "slt": 0x17,    # Set Less Than
    "mul": 0x18,    # Multiplicação
    "div": 0x19,    # Divisão
    "mod": 0x1A,    # Módulo
    "neg": 0x1B,    # Negação
    "inc": 0x1C,    # Incremento
    "dec": 0x1D,    # Decremento
    "nop": 0x1E,    # No Operation
    "halt": 0xFF,   # Halt (todos os bits em 1)
}

# Classificação por tipo de instrução
INSTR_TYPE_3REG = {
    "add", "sub", "xor", "or", "and",
    "asl", "asr", "lsl", "lsr",
    "slt", "mul", "div", "mod"
}

# CORRIGIDO: zeros, inc, dec agora classificados corretamente
INSTR_TYPE_2REG = {
    "passnota", "neg", "passa", "load", "store",
    "inc", "dec"  # CORRIGIDO: inc e dec são type_2reg
}

INSTR_TYPE_1REG = {
    "jr", "zeros"  # CORRIGIDO: zeros é type_1reg
}

INSTR_TYPE_IMM16 = {
    "lch", "lcl"
}

INSTR_TYPE_BRANCH = {
    "beq", "bne"
}

INSTR_TYPE_JUMP = {
    "jal", "j"
}

INSTR_TYPE_NONE = {
    "nop", "halt"
}

# Constantes
MAX_REGISTER = 31
MAX_ADDRESS_16 = 0xFFFF
MAX_ADDRESS_24 = 0xFFFFFF
MAX_CONST16 = 0xFFFF
MAX_OFFSET8 = 0xFF
