"""
parser.py - Análise Léxica e Sintática

Processa linhas de assembly, extrai labels e tokens.
"""

import re

from opcodes import MAX_ADDRESS_16, OPCODES


class AssemblyError(Exception):
    """Exceção para erros de assembly."""

    def __init__(self, msg, lineno=None, line=None):
        self.msg = msg
        self.lineno = lineno
        self.line = line
        super().__init__(self._format())

    def _format(self):
        prefix = f"[Linha {self.lineno}] " if self.lineno else ""
        suffix = f"\n  > {self.line.strip()}" if self.line else ""
        return prefix + self.msg + suffix


def preprocess_line(raw):
    """Remove comentários e normaliza espaços."""
    # Remove comentários (# ou ;)
    line = raw.split("#", 1)[0].split(";", 1)[0]
    # Substitui vírgulas por espaços
    line = line.replace(",", " ")
    return line.strip()


def tokenize(line):
    """Divide linha em tokens."""
    if not line:
        return []
    return re.split(r"\s+", line.strip())


def parse_register(token, lineno=None, line=None):
    """
    Converte token 'rN' para número do registrador (0-31).

    Exemplos:
        r0 -> 0
        r15 -> 15
        r31 -> 31
    """
    if not isinstance(token, str):
        raise AssemblyError(f"Registrador inválido: {token}", lineno, line)

    token = token.strip().lower()

    if not token.startswith("r"):
        raise AssemblyError(
            f"Registrador deve começar com 'r': {token}", lineno, line
        )

    try:
        n = int(token[1:])
    except ValueError:
        raise AssemblyError(f"Registrador inválido: {token}", lineno, line)

    if not (0 <= n <= 31):
        raise AssemblyError(
            f"Registrador fora do intervalo 0-31: {token}", lineno, line
        )

    return n


def parse_number(token, lineno=None, line=None):
    """
    Tenta converter token para número inteiro.
    Suporta decimal, hexadecimal (0x) e binário (0b).
    Retorna None se for uma label.
    """
    if token is None:
        return None

    token = token.strip()

    try:
        return int(token, 0)  # Detecta base automaticamente
    except ValueError:
        return None  # É uma label


class Parser:
    """Parser de assembly UFLA-RISC."""

    def __init__(self):
        self.instructions = []
        self.labels = {}
        self.current_address = 0

    def first_pass(self, lines):
        """
        Primeira passagem: identifica labels e instruções.

        Retorna: (lista_instruções, dicionário_labels)
        """
        self.instructions = []
        self.labels = {}
        self.current_address = 0

        for lineno, raw in enumerate(lines, start=1):
            line = preprocess_line(raw)

            if not line:
                continue

            tokens = tokenize(line)
            if not tokens:
                continue

            # Diretiva 'address'
            if tokens[0].lower() == "address":
                self._process_address_directive(tokens, lineno, raw)
                continue

            # Label (termina com ':')
            if line.endswith(":"):
                self._process_label(line, lineno, raw)
                continue

            # Label + instrução na mesma linha
            if ":" in line:
                line = self._process_inline_label(line, lineno, raw)
                if not line:
                    continue
                tokens = tokenize(line)

            # Instrução
            self._process_instruction(tokens, lineno, raw)

        return self.instructions, self.labels

    def _process_address_directive(self, tokens, lineno, raw):
        """Processa diretiva 'address'."""
        if len(tokens) < 2:
            raise AssemblyError(
                "Diretiva 'address' exige um argumento", lineno, raw
            )

        val = parse_number(tokens[1], lineno, raw)

        if val is None:
            # Tentar como binário
            try:
                val = int(tokens[1], 2)
            except ValueError:
                raise AssemblyError(
                    f"Endereço inválido: {tokens[1]}", lineno, raw
                )

        if not (0 <= val <= MAX_ADDRESS_16):
            raise AssemblyError(
                f"Endereço fora do intervalo 0-65535: {val}", lineno, raw
            )

        self.current_address = val

    def _process_label(self, line, lineno, raw):
        """Processa label isolada."""
        label = line[:-1].strip()

        if not label:
            raise AssemblyError("Label vazia", lineno, raw)

        if label in self.labels:
            raise AssemblyError(f"Label duplicada: {label}", lineno, raw)

        self.labels[label] = self.current_address

    def _process_inline_label(self, line, lineno, raw):
        """Processa label + instrução na mesma linha."""
        parts = line.split(":", 1)
        label = parts[0].strip()
        rest = parts[1].strip()

        if not label:
            raise AssemblyError("Label vazia", lineno, raw)

        if label in self.labels:
            raise AssemblyError(f"Label duplicada: {label}", lineno, raw)

        self.labels[label] = self.current_address

        return rest

    def _process_instruction(self, tokens, lineno, raw):
        """Processa instrução."""
        op = tokens[0].lower()

        if op.startswith("#") or not op:
            return

        if op not in OPCODES:
            raise AssemblyError(f"Instrução desconhecida: {op}", lineno, raw)

        args = tokens[1:]

        self.instructions.append({
            "op": op,
            "args": args,
            "lineno": lineno,
            "raw": raw,
            "address": self.current_address
        })

        self.current_address += 1
