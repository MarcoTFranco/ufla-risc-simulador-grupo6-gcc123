"""
encoder.py - Codificador de Instruções

Converte instruções assembly para código de máquina binário.
"""

from parser import AssemblyError, parse_number, parse_register

from opcodes import *


class InstructionEncoder:
    """Codifica instruções UFLA-RISC em binário."""

    def __init__(self, labels):
        self.labels = labels

    def encode(self, instruction):
        """
        Codifica uma instrução em binário de 32 bits.

        Retorna: inteiro de 32 bits
        """
        op = instruction["op"]
        args = instruction["args"]
        lineno = instruction["lineno"]
        raw = instruction["raw"]

        opcode = OPCODES[op]

        # HALT: todos os bits em 1
        if op == "halt":
            return 0xFFFFFFFF

        # NOP: apenas opcode
        if op == "nop":
            return opcode << 24

        # Instruções de 3 registradores
        if op in INSTR_TYPE_3REG:
            return self._encode_3reg(opcode, args, lineno, raw)

        # Instruções de 2 registradores
        if op in INSTR_TYPE_2REG:
            return self._encode_2reg(opcode, args, lineno, raw)

        # Instruções de 1 registrador
        if op in INSTR_TYPE_1REG:
            return self._encode_1reg(opcode, args, lineno, raw)

        # Instruções com imediato 16 bits
        if op in INSTR_TYPE_IMM16:
            return self._encode_imm16(opcode, args, lineno, raw)

        # Instruções de branch
        if op in INSTR_TYPE_BRANCH:
            return self._encode_branch(opcode, args, lineno, raw)

        # Instruções de jump
        if op in INSTR_TYPE_JUMP:
            return self._encode_jump(opcode, args, lineno, raw)

        raise AssemblyError(
            f"Tipo de instrução não reconhecido: {op}", lineno, raw)

    def _encode_3reg(self, opcode, args, lineno, raw):
        """Formato: opcode(31-24) | ra(23-16) | rb(15-8) | rc(7-0)"""
        if len(args) < 3:
            raise AssemblyError("Instrução exige 3 registradores", lineno, raw)

        rc = parse_register(args[0], lineno, raw)
        ra = parse_register(args[1], lineno, raw)
        rb = parse_register(args[2], lineno, raw)

        return (opcode << 24) | (ra << 16) | (rb << 8) | rc

    def _encode_2reg(self, opcode, args, lineno, raw):
        """Formato: opcode(31-24) | ra(23-16) | rc(7-0)"""
        if len(args) < 2:
            raise AssemblyError("Instrução exige 2 registradores", lineno, raw)

        rc = parse_register(args[0], lineno, raw)
        ra = parse_register(args[1], lineno, raw)

        return (opcode << 24) | (ra << 16) | rc

    def _encode_1reg(self, opcode, args, lineno, raw):
        """Formato: opcode(31-24) | rc(7-0)"""
        if len(args) < 1:
            raise AssemblyError("Instrução exige 1 registrador", lineno, raw)

        rc = parse_register(args[0], lineno, raw)

        return (opcode << 24) | rc

    def _encode_imm16(self, opcode, args, lineno, raw):
        """Formato: opcode(31-24) | const16(23-8) | rc(7-0)"""
        if len(args) < 2:
            raise AssemblyError(
                "Instrução exige registrador e constante", lineno, raw)

        rc = parse_register(args[0], lineno, raw)
        val = parse_number(args[1], lineno, raw)

        if val is None:
            raise AssemblyError(f"Constante inválida: {args[1]}", lineno, raw)

        if not (0 <= val <= MAX_CONST16):
            raise AssemblyError(
                f"Constante fora do intervalo 0-65535: {val}", lineno, raw
            )

        const16 = val & 0xFFFF

        return (opcode << 24) | (const16 << 8) | rc

    def _encode_branch(self, opcode, args, lineno, raw):
        """Formato: opcode(31-24) | ra(23-16) | rb(15-8) | end(7-0)"""
        if len(args) < 3:
            raise AssemblyError(
                "Branch exige 2 registradores e endereço", lineno, raw)

        ra = parse_register(args[0], lineno, raw)
        rb = parse_register(args[1], lineno, raw)

        val = parse_number(args[2], lineno, raw)

        if val is None:
            # É uma label
            if args[2] not in self.labels:
                raise AssemblyError(
                    f"Label não encontrada: {args[2]}", lineno, raw)
            val = self.labels[args[2]]

        if not (0 <= val <= MAX_OFFSET8):
            raise AssemblyError(
                f"Endereço de branch fora do intervalo 0-255: {val}", lineno, raw
            )

        end = val & 0xFF

        return (opcode << 24) | (ra << 16) | (rb << 8) | end

    def _encode_jump(self, opcode, args, lineno, raw):
        """Formato: opcode(31-24) | endereço(23-0)"""
        if len(args) < 1:
            raise AssemblyError("Jump exige endereço", lineno, raw)

        val = parse_number(args[0], lineno, raw)

        if val is None:
            # É uma label
            if args[0] not in self.labels:
                raise AssemblyError(
                    f"Label não encontrada: {args[0]}", lineno, raw)
            val = self.labels[args[0]]

        if not (0 <= val <= MAX_ADDRESS_24):
            raise AssemblyError(
                f"Endereço de jump fora do intervalo 0-16777215: {val}", lineno, raw
            )

        end = val & 0xFFFFFF

        return (opcode << 24) | end
