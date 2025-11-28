"""
alu.py - Unidade Lógica e Aritmética (ALU) - VERSÃO CORRIGIDA

Implementa todas as operações de cálculo (ALU, shifts, divisão, etc)
e gerencia atualização de flags.

"""

from utils import MASK32, to_s32, to_u32


class ALUException(Exception):
    """Exceção para erros da ALU (divisão por zero, etc)."""
    pass


class ALU:
    """Unidade Lógica e Aritmética do UFLA-RISC."""

    def __init__(self):
        """Inicializa ALU."""
        self.last_result = 0
        self.flags_neg = 0
        self.flags_zero = 0
        self.flags_carry = 0
        self.flags_overflow = 0

    # ==================== FLAGS ====================

    def get_flags(self):
        """Retorna flags como dicionário."""
        return {
            'neg': self.flags_neg,
            'zero': self.flags_zero,
            'carry': self.flags_carry,
            'overflow': self.flags_overflow
        }

    def set_flags_dict(self, flags_dict):
        """Define flags a partir de dicionário."""
        self.flags_neg = flags_dict.get('neg', 0)
        self.flags_zero = flags_dict.get('zero', 0)
        self.flags_carry = flags_dict.get('carry', 0)
        self.flags_overflow = flags_dict.get('overflow', 0)

    def clear_flags(self):
        """Zera todos os flags."""
        self.flags_neg = self.flags_zero = 0
        self.flags_carry = self.flags_overflow = 0

    def update_flags_arithmetic(self, result, a, b, is_sub=False):
        """
        Atualiza flags para operações aritméticas (ADD, SUB).

        Flags afetados:
        - neg: bit 31 do resultado
        - zero: resultado == 0
        - carry: overflow do cálculo
        - overflow: overflow aritmético (two's complement)
        """
        result_u32 = to_u32(result)

        # Flag ZERO
        self.flags_zero = 1 if result_u32 == 0 else 0

        # Flag NEG
        self.flags_neg = 1 if (result_u32 & 0x80000000) else 0

        # Flag CARRY
        if is_sub:
            self.flags_carry = 1 if (a < b) else 0
        else:
            self.flags_carry = 1 if (result > MASK32) else 0

        # Flag OVERFLOW (two's complement overflow)
        a_s32 = to_s32(a)
        b_s32 = to_s32(b)
        result_s32 = to_s32(result_u32)

        if is_sub:
            # Overflow na subtração: (a >= 0 && b < 0 && result < 0) ||
            #                        (a < 0 && b >= 0 && result >= 0)
            self.flags_overflow = 1 if (
                (a_s32 >= 0 and b_s32 < 0 and result_s32 < 0) or
                (a_s32 < 0 and b_s32 >= 0 and result_s32 >= 0)
            ) else 0
        else:
            # Overflow na adição: (a >= 0 && b >= 0 && result < 0) ||
            #                     (a < 0 && b < 0 && result >= 0)
            self.flags_overflow = 1 if (
                (a_s32 >= 0 and b_s32 >= 0 and result_s32 < 0) or
                (a_s32 < 0 and b_s32 < 0 and result_s32 >= 0)
            ) else 0

    def update_flags_logical(self, result):
        """
        Atualiza flags para operações lógicas (XOR, OR, AND, NOT).

        Flags afetados:
        - neg: bit 31 do resultado
        - zero: resultado == 0
        - carry: sempre 0
        - overflow: sempre 0
        """
        result_u32 = to_u32(result)
        self.flags_zero = 1 if result_u32 == 0 else 0
        self.flags_neg = 1 if (result_u32 & 0x80000000) else 0
        self.flags_carry = 0
        self.flags_overflow = 0

    # ==================== OPERAÇÕES ALU ====================

    def add(self, a, b):
        """Adição com atualização de flags."""
        result = to_u32(a + b)
        self.last_result = result
        self.update_flags_arithmetic(a + b, a, b, is_sub=False)
        return result

    def sub(self, a, b):
        """Subtração com atualização de flags."""
        result = to_u32(a - b)
        self.last_result = result
        self.update_flags_arithmetic(a - b, a, b, is_sub=True)
        return result

    def xor(self, a, b):
        """XOR lógico com atualização de flags."""
        result = to_u32(a ^ b)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def or_op(self, a, b):
        """OR lógico com atualização de flags."""
        result = to_u32(a | b)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def and_op(self, a, b):
        """AND lógico com atualização de flags."""
        result = to_u32(a & b)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def not_op(self, a):
        """NOT lógico (complemento) com atualização de flags."""
        result = to_u32(~a)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def zeros(self):
        """Retorna zero e atualiza flags."""
        self.last_result = 0
        self.flags_zero = 1
        self.flags_neg = 0
        self.flags_carry = 0
        self.flags_overflow = 0
        return 0

    # ==================== OPERAÇÕES ESPECIAIS ====================

    def mul(self, a, b):
        """Multiplicação (com truncamento para 32 bits)."""
        result = to_u32(a * b)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def div(self, a, b):
        """Divisão com sinal."""
        if b == 0:
            print("WARNING: Divisão por zero detectada! Retornando 0")
            self.last_result = 0
            self.flags_zero = 1
            self.flags_neg = 0
            self.flags_carry = 0
            self.flags_overflow = 0
            return 0
            # Ou lançar exceção (descomente para modo strict):
            # raise ALUException("Divisão por zero")

        a_s32 = to_s32(a)
        b_s32 = to_s32(b)
        result = to_u32(a_s32 // b_s32)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def mod(self, a, b):
        """Módulo com sinal."""
        if b == 0:
            # Comportamento alternativo: retornar 0 com warning
            print("⚠️  WARNING: Módulo por zero detectado! Retornando 0")
            self.last_result = 0
            self.flags_zero = 1
            self.flags_neg = 0
            self.flags_carry = 0
            self.flags_overflow = 0
            return 0
            # Ou lançar exceção (descomente para modo strict):
            # raise ALUException("Módulo por zero")

        a_s32 = to_s32(a)
        b_s32 = to_s32(b)
        result = to_u32(a_s32 % b_s32)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def slt(self, a, b):
        """Set Less Than (a < b ? 1 : 0)."""
        a_s32 = to_s32(a)
        b_s32 = to_s32(b)
        result = 1 if a_s32 < b_s32 else 0
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def inc(self, a):
        """Incremento (a + 1)."""
        result = to_u32(a + 1)
        self.last_result = result
        self.update_flags_arithmetic(a + 1, a, 1, is_sub=False)
        return result

    def dec(self, a):
        """Decremento (a - 1)."""
        result = to_u32(a - 1)
        self.last_result = result
        self.update_flags_arithmetic(a - 1, a, 1, is_sub=True)
        return result

    def neg(self, a):
        """Negação (-a)."""
        result = to_u32(-to_s32(a))
        self.last_result = result
        self.update_flags_arithmetic(-to_s32(a), 0, a, is_sub=True)
        return result

    def copy(self, a):
        """Cópia (resultado = a)."""
        result = to_u32(a)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    # ==================== OPERAÇÕES DE SHIFT ====================

    def asl(self, value, shift_amount):
        """Arithmetic Shift Left."""
        shift = shift_amount & 0x1F
        result = to_u32(value << shift)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def asr(self, value, shift_amount):
        """Arithmetic Shift Right (preserva bit de sinal)."""
        shift = shift_amount & 0x1F
        value_s32 = to_s32(value)
        result = to_u32(value_s32 >> shift)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def lsl(self, value, shift_amount):
        """Logical Shift Left."""
        shift = shift_amount & 0x1F
        result = to_u32(value << shift)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    def lsr(self, value, shift_amount):
        """Logical Shift Right."""
        shift = shift_amount & 0x1F
        result = to_u32(value >> shift)
        self.last_result = result
        self.update_flags_logical(result)
        return result

    # ==================== OPERAÇÕES COM CONSTANTES ====================

    def load_const_high(self, reg_value, const16):
        """Carrega constante nos 16 bits altos."""
        result = to_u32((const16 << 16) | (reg_value & 0x0000FFFF))
        return result

    def load_const_low(self, reg_value, const16):
        """Carrega constante nos 16 bits baixos."""
        result = to_u32((reg_value & 0xFFFF0000) | const16)
        return result

    # ==================== DEBUG ====================

    def print_flags(self):
        """Imprime estado dos flags."""
        print(f"Flags: neg={self.flags_neg}, zero={self.flags_zero}, "
              f"carry={self.flags_carry}, overflow={self.flags_overflow}")

    def print_last_result(self):
        """Imprime último resultado."""
        print(f"Último resultado: 0x{self.last_result:08x} "
              f"(u32: {self.last_result}, s32: {to_s32(self.last_result)})")
