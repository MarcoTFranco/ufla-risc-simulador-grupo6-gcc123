"""
instruction_decoder.py - Decodificador de Instruções

Extrai e interpreta campos de instruções UFLA-RISC.
Define mapeamento de opcodes e tipos de instrução.
"""

from utils import MASK8, MASK16, to_u32


class InstructionDecoder:
    """Decodificador de instruções UFLA-RISC."""

    # Mapeamento de opcodes para nomes
    OPCODE_NAMES = {
        0x01: 'ADD',    0x02: 'SUB',    0x03: 'ZEROS',  0x04: 'XOR',
        0x05: 'OR',     0x06: 'NOT',    0x07: 'AND',    0x08: 'ASL',
        0x09: 'ASR',    0x0A: 'LSL',    0x0B: 'LSR',    0x0C: 'PASSA',
        0x0E: 'LCH',    0x0F: 'LCL',    0x10: 'LOAD',   0x11: 'STORE',
        0x12: 'JAL',    0x13: 'JR',     0x14: 'BEQ',    0x15: 'BNE',
        0x16: 'J',      0x17: 'SLT',    0x18: 'MUL',    0x19: 'DIV',
        0x1A: 'MOD',    0x1B: 'NEG',    0x1C: 'INC',    0x1D: 'DEC',
        0x1E: 'NOP',    0xFF: 'HALT'
    }

    # Tipos de instrução
    INSTR_TYPE_3REG = 'type_3reg'      # rc, ra, rb
    INSTR_TYPE_2REG = 'type_2reg'      # rc, ra
    INSTR_TYPE_1REG = 'type_1reg'      # rc
    INSTR_TYPE_2REG_IMM = 'type_2reg_imm'  # rc, const16
    INSTR_TYPE_2REG_ADDR = 'type_2reg_addr'  # ra, rb, endereço
    INSTR_TYPE_BRANCH = 'type_branch'  # ra, rb, endereço
    INSTR_TYPE_JUMP = 'type_jump'      # endereço
    INSTR_TYPE_NONE = 'type_none'      # Sem operandos

    # Classificação de opcodes por tipo
    OPCODE_TYPES = {
        # 3 registradores
        0x01: INSTR_TYPE_3REG,  # ADD
        0x02: INSTR_TYPE_3REG,  # SUB
        0x04: INSTR_TYPE_3REG,  # XOR
        0x05: INSTR_TYPE_3REG,  # OR
        0x07: INSTR_TYPE_3REG,  # AND
        0x08: INSTR_TYPE_3REG,  # ASL
        0x09: INSTR_TYPE_3REG,  # ASR
        0x0A: INSTR_TYPE_3REG,  # LSL
        0x0B: INSTR_TYPE_3REG,  # LSR
        0x18: INSTR_TYPE_3REG,  # MUL
        0x19: INSTR_TYPE_3REG,  # DIV
        0x1A: INSTR_TYPE_3REG,  # MOD

        # 2 registradores
        0x06: INSTR_TYPE_2REG,  # NOT
        0x0C: INSTR_TYPE_2REG,  # PASSA
        0x1B: INSTR_TYPE_2REG,  # NEG
        0x10: INSTR_TYPE_2REG,  # LOAD
        0x1C: INSTR_TYPE_2REG,  # INC - CORRIGIDO
        0x1D: INSTR_TYPE_2REG,  # DEC - CORRIGIDO

        # 2 registradores com imediato
        0x0E: INSTR_TYPE_2REG_IMM,  # LCH
        0x0F: INSTR_TYPE_2REG_IMM,  # LCL

        # STORE (ra -> mem[rc])
        0x11: 'type_store',  # STORE rc, ra

        # 1 registrador - CORRIGIDO: ZEROS agora é type_1reg
        0x03: INSTR_TYPE_1REG,  # ZEROS rc
        0x13: INSTR_TYPE_1REG,  # JR

        # Condicional (branch)
        0x14: INSTR_TYPE_BRANCH,  # BEQ
        0x15: INSTR_TYPE_BRANCH,  # BNE

        # Jump (incondicional)
        0x12: INSTR_TYPE_JUMP,  # JAL
        0x16: INSTR_TYPE_JUMP,  # J

        # Sem operandos
        0x1E: INSTR_TYPE_NONE,  # NOP
        0xFF: INSTR_TYPE_NONE,  # HALT
    }

    # Operações que afetam flags
    AFFECTS_FLAGS = {
        0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x17, 0x18,
        0x19, 0x1A, 0x1B, 0x1C, 0x1D
    }

    def __init__(self):
        """Inicializa decodificador."""
        pass

    # ==================== DECODIFICAÇÃO ====================

    def decode(self, instruction):
        """
        Decodifica instrução completa.
        Retorna dicionário com todos os campos extraídos.

        CORREÇÃO: Adicionado branch_offset separado para branches de 8 bits.
        """
        instruction = to_u32(instruction)

        opcode = self.extract_opcode(instruction)

        return {
            'raw': instruction,
            'opcode': opcode,
            'ra': self.extract_ra(instruction),
            'rb': self.extract_rb(instruction),
            'rc': self.extract_rc(instruction),
            'const16': self.extract_const16(instruction),
            'address': self.extract_address(instruction),
            'branch_offset': self.extract_branch_offset(instruction),  # NOVO
            'type': self.get_instruction_type(opcode),
            'mnemonic': self.get_mnemonic(opcode)
        }

    # ==================== EXTRAÇÃO DE CAMPOS ====================

    def extract_opcode(self, instruction):
        """Extrai opcode (bits 31-24)."""
        return (instruction >> 24) & MASK8

    def extract_ra(self, instruction):
        """Extrai registrador RA (bits 23-16)."""
        return (instruction >> 16) & MASK8

    def extract_rb(self, instruction):
        """Extrai registrador RB (bits 15-8)."""
        return (instruction >> 8) & MASK8

    def extract_rc(self, instruction):
        """Extrai registrador RC (bits 7-0)."""
        return instruction & MASK8

    def extract_const16(self, instruction):
        """Extrai constante de 16 bits (bits 23-8)."""
        return (instruction >> 8) & MASK16

    def extract_address(self, instruction):
        """Extrai endereço de 24 bits (bits 23-0)."""
        return instruction & 0xFFFFFF

    def extract_branch_offset(self, instruction):
        """
        Extrai offset de 8 bits para branches (bits 7-0).
        NOVO: Branches usam apenas 8 bits, não 24.
        """
        return instruction & 0xFF

    # ==================== INFORMAÇÕES ====================

    def get_mnemonic(self, opcode):
        """Retorna mnemônico da instrução."""
        return self.OPCODE_NAMES.get(opcode, 'UNKNOWN')

    def get_instruction_type(self, opcode):
        """Retorna tipo de instrução."""
        return self.OPCODE_TYPES.get(opcode, 'unknown')

    def affects_flags(self, opcode):
        """Verifica se instrução afeta flags."""
        return opcode in self.AFFECTS_FLAGS

    # ==================== VALIDAÇÃO ====================

    def is_valid_opcode(self, opcode):
        """Verifica se opcode é válido."""
        return opcode in self.OPCODE_NAMES

    def is_alu_operation(self, opcode):
        """Verifica se é operação ALU."""
        return opcode in {0x01, 0x02, 0x04, 0x05, 0x07, 0x17, 0x18, 0x19, 0x1A}

    def is_shift_operation(self, opcode):
        """Verifica se é operação de shift."""
        return opcode in {0x08, 0x09, 0x0A, 0x0B}

    def is_memory_operation(self, opcode):
        """Verifica se é operação de memória."""
        return opcode in {0x10, 0x11}

    def is_branch_operation(self, opcode):
        """Verifica se é operação de branch."""
        return opcode in {0x12, 0x13, 0x14, 0x15, 0x16}

    def is_load_operation(self, opcode):
        """Verifica se é LOAD."""
        return opcode == 0x10

    def is_store_operation(self, opcode):
        """Verifica se é STORE."""
        return opcode == 0x11

    # ==================== FORMATAÇÃO ====================

    def format_instruction(self, decoded_instr):
        """Formata instrução decodificada para exibição."""
        op = decoded_instr['opcode']
        ra = decoded_instr['ra']
        rb = decoded_instr['rb']
        rc = decoded_instr['rc']
        const16 = decoded_instr['const16']
        addr = decoded_instr['address']
        branch_off = decoded_instr['branch_offset']
        mnemonic = decoded_instr['mnemonic']
        instr_type = decoded_instr['type']

        # Limitar ra, rb, rc a 31 (válido)
        ra = min(ra, 31)
        rb = min(rb, 31)
        rc = min(rc, 31)

        result = f"{mnemonic:8s}"

        # Formatar operandos de acordo com tipo
        if instr_type == self.INSTR_TYPE_3REG:
            result += f" R{rc}, R{ra}, R{rb}"
        elif instr_type == self.INSTR_TYPE_2REG:
            result += f" R{rc}, R{ra}"
        elif instr_type == self.INSTR_TYPE_2REG_IMM:
            result += f" R{rc}, 0x{const16:04x}"
        elif instr_type == 'type_store':
            result += f" R{rc}, R{ra}"
        elif instr_type == self.INSTR_TYPE_1REG:
            result += f" R{rc}"
        elif instr_type == self.INSTR_TYPE_BRANCH:
            # CORRIGIDO: Usar branch_offset (8 bits) ao invés de address (24 bits)
            result += f" R{ra}, R{rb}, 0x{branch_off:02x}"
        elif instr_type == self.INSTR_TYPE_JUMP:
            result += f" 0x{addr:06x}"

        return result

    # ==================== DEBUG ====================

    def print_instruction(self, instruction):
        """Imprime instrução decodificada."""
        decoded = self.decode(instruction)
        formatted = self.format_instruction(decoded)

        print(f"Instrução: {hex(instruction)}")
        print(f"  Opcode: {hex(decoded['opcode'])} ({decoded['mnemonic']})")
        print(f"  RA: R{min(decoded['ra'], 31)}")
        print(f"  RB: R{min(decoded['rb'], 31)}")
        print(f"  RC: R{min(decoded['rc'], 31)}")
        print(f"  Tipo: {decoded['type']}")
        print(f"  Formatado: {formatted}")
