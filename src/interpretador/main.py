"""
main.py - Interface de Linha de Comando

Ponto de entrada para o interpretador/assembler UFLA-RISC.
"""

import os
import sys
from parser import AssemblyError

from assembler import Assembler

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_usage():
    """Imprime instruções de uso."""
    print("=" * 70)
    print("INTERPRETADOR/ASSEMBLER UFLA-RISC")
    print("=" * 70)
    print("Instruções Suportadas:")
    print("  • Básicas: add, sub, zeros, xor, or, passnota, and")
    print("  • Shifts: asl, asr, lsl, lsr")
    print("  • Memória: load, store, passa")
    print("  • Constantes: lch, lcl")
    print("  • Controle: jal, jr, beq, bne, j, halt")
    print("  • Adicionais: slt, mul, div, mod, neg, inc, dec, nop")
    print("=" * 70)


def main():
    """Função principal."""
    if len(sys.argv) < 3:
        print_usage()
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        # Criar assembler
        assembler = Assembler()

        # Montar arquivo
        print(f"Montando '{input_file}'...")
        binary_lines = assembler.assemble_file(input_file)

        # Escrever saída
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(binary_lines))

        # Estatísticas
        stats = assembler.get_stats()

        print(f"✓ Montagem concluída com sucesso!")
        print(f"✓ Arquivo gerado: {output_file}")
        print(f"✓ Total de instruções: {stats['instructions']}")
        print(f"✓ Total de labels: {stats['labels']}")

        if stats['label_list']:
            print(f"✓ Labels encontradas: {', '.join(stats['label_list'])}")

        return 0

    except AssemblyError as e:
        print(f"\n❌ ERRO DE MONTAGEM:")
        print(str(e))
        return 1

    except Exception as e:
        print(f"\n❌ ERRO INESPERADO:")
        print(str(e))
        import traceback
        traceback.print_exc()
        return 1


# Para usar:
# python src/interpretador/main.py exemplos/programa.asm binarios/programa.bin
if __name__ == "__main__":
    sys.exit(main())
