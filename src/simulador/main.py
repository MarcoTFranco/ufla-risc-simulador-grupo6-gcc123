"""
main.py - Interface de linha de comando OTIMIZADA

"""

import sys

from simulator import Simulator


def main():
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("=" * 70)
        print("SIMULADOR UFLA-RISC")
        print("=" * 70)
        print("Uso: python main.py <arquivo_binario> [--verbose]")
        print("\nExemplos:")
        print("  python main.py binarios/programa.bin")
        print("  python main.py binarios/programa.bin --verbose")
        print("\nOpções:")
        print("  --verbose, -v : Mostra todos os ciclos (padrão: apenas resumo)")
        print("=" * 70)
        exit(1)

    # Processar argumentos
    input_file = sys.argv[1]
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    # Criar simulador com modo verboso
    sim = Simulator(verbose=verbose)

    # Carregar programa
    print(f"Carregando programa: {input_file}")
    instr_count = sim.memory.load_program_from_text(input_file)

    if instr_count == 0:
        print("❌ Nenhuma instrução carregada. Encerrando.")
        exit(1)

    # Executar simulação
    sim.run()

    # Mostrar estado final
    print("\n" + "="*70)
    print("ESTADO FINAL DA CPU")
    print("="*70)
    sim.cpu.print_registers(show_zero=False)

    print("\n" + "="*70)
    print("MEMÓRIA FINAL (posições não-zero)")
    print("="*70)
    sim.memory.print_non_zero(limit=20)

# Modo limpo (recomendado)
# python main.py binarios/teste.bin


# Modo debug completo
# python main.py binarios/teste.bin --verbose
if __name__ == '__main__':
    main()
