"""
assembler.py - Assembler Principal

Orquestra o processo de montagem (assembly → binário).
"""

from parser import AssemblyError, Parser

from encoder import InstructionEncoder


class Assembler:
    """Assembler UFLA-RISC."""

    def __init__(self):
        self.parser = Parser()
        self.encoder = None
        self.instructions = []
        self.labels = {}

    def assemble_file(self, input_filename):
        """
        Monta arquivo assembly completo.

        Retorna: lista de strings binárias de 32 bits
        """
        # Ler arquivo
        try:
            with open(input_filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise AssemblyError(f"Arquivo não encontrado: {input_filename}")
        except Exception as e:
            raise AssemblyError(f"Erro ao ler arquivo: {e}")

        return self.assemble_lines(lines)

    def assemble_lines(self, lines):
        """
        Monta lista de linhas de assembly.

        Retorna: lista de strings binárias de 32 bits
        """
        # Primeira passagem: parse
        self.instructions, self.labels = self.parser.first_pass(lines)

        # Criar encoder com labels
        self.encoder = InstructionEncoder(self.labels)

        # Segunda passagem: codificação
        binary_lines = []
        for instr in self.instructions:
            encoded = self.encoder.encode(instr)
            binary_lines.append(f"{encoded:032b}")

        return binary_lines

    def get_stats(self):
        """Retorna estatísticas da montagem."""
        return {
            "instructions": len(self.instructions),
            "labels": len(self.labels),
            "label_list": list(self.labels.keys())
        }
