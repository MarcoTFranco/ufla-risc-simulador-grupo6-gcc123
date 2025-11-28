"""
memory.py - Gerenciamento de Memória

Abstração completa da memória do processador UFLA-RISC.
Fornece leitura/escrita, carregamento de programas e validação.
"""

from utils import MEMORY_SIZE, to_u32, clamp_address, is_valid_address


class Memory:
    """Gerencia memória do processador UFLA-RISC (64K palavras)."""
    
    def __init__(self):
        """Inicializa memória com 64K palavras zeradas."""
        self.data = [0] * MEMORY_SIZE
        self.breakpoints = set()
    
    # ==================== LEITURA E ESCRITA ====================
    
    def read(self, address):
        """Lê palavra na memória."""
        address = clamp_address(address) & 0xFFFF
        return self.data[address]
    
    def write(self, address, value):
        """Escreve palavra na memória."""
        address = clamp_address(address) & 0xFFFF
        self.data[address] = to_u32(value)
    
    def read_word(self, address):
        """Alias para read (mais explícito)."""
        return self.read(address)
    
    def write_word(self, address, value):
        """Alias para write (mais explícito)."""
        self.write(address, value)
    
    # ==================== OPERAÇÕES EM BLOCO ====================
    
    def read_block(self, start_address, count):
        """Lê bloco de palavras consecutivas."""
        start_address = clamp_address(start_address) & 0xFFFF
        result = []
        for i in range(count):
            addr = (start_address + i) & 0xFFFF
            result.append(self.data[addr])
        return result
    
    def write_block(self, start_address, values):
        """Escreve bloco de palavras consecutivas."""
        start_address = clamp_address(start_address) & 0xFFFF
        for i, value in enumerate(values):
            addr = (start_address + i) & 0xFFFF
            self.data[addr] = to_u32(value)
    
    # ==================== CARREGAMENTO DE PROGRAMAS ====================
    
    def load_program_from_text(self, filename):
        """
        Carrega programa de arquivo texto com instruções binárias.
        
        Formato:
            address <endereco_binário>
            <instrução_binária_32bits>
            <instrução_binária_32bits>
            ...
        
        Retorna número de instruções carregadas.
        """
        current_address = 0
        instruction_count = 0
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Ignorar linhas vazias e comentários
                    if not line or line.startswith('#'):
                        continue
                    
                    # Processar diretiva "address"
                    if line.lower().startswith('address'):
                        parts = line.split()
                        if len(parts) >= 2:
                            try:
                                current_address = int(parts[1], 2)
                            except ValueError:
                                print(f"⚠️  Linha {line_num}: endereço inválido em {parts[1]}")
                        continue
                    
                    # Processar instrução (32 bits em binário)
                    if len(line) == 32 and all(c in '01' for c in line):
                        instruction = int(line, 2)
                        self.write(current_address, instruction)
                        current_address = (current_address + 1) & 0xFFFF
                        instruction_count += 1
                    else:
                        if line and not line.startswith('address'):
                            print(f"⚠️  Linha {line_num}: instrução inválida: {line}")
            
            print(f"✓ Programa carregado: {instruction_count} instruções")
            return instruction_count
            
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo '{filename}' não encontrado")
            return 0
        except Exception as e:
            print(f"❌ Erro ao carregar programa: {e}")
            return 0
    
    def load_program_from_binary(self, filename):
        """
        Carrega programa de arquivo binário.
        Cada instrução é um inteiro de 32 bits.
        """
        instruction_count = 0
        current_address = 0
        
        try:
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(4)
                    if not data:
                        break
                    
                    if len(data) < 4:
                        print(f"⚠️  Instrução incompleta na posição {current_address}")
                        break
                    
                    # Converter bytes para inteiro (big-endian)
                    instruction = int.from_bytes(data, byteorder='big')
                    self.write(current_address, instruction)
                    current_address = (current_address + 1) & 0xFFFF
                    instruction_count += 1
            
            print(f"✓ Programa binário carregado: {instruction_count} instruções")
            return instruction_count
            
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo '{filename}' não encontrado")
            return 0
        except Exception as e:
            print(f"❌ Erro ao carregar programa binário: {e}")
            return 0
    
    # ==================== BREAKPOINTS ====================
    
    def add_breakpoint(self, address):
        """Adiciona breakpoint em endereço."""
        address = clamp_address(address) & 0xFFFF
        self.breakpoints.add(address)
    
    def remove_breakpoint(self, address):
        """Remove breakpoint de endereço."""
        address = clamp_address(address) & 0xFFFF
        self.breakpoints.discard(address)
    
    def has_breakpoint(self, address):
        """Verifica se há breakpoint em endereço."""
        address = clamp_address(address) & 0xFFFF
        return address in self.breakpoints
    
    def clear_breakpoints(self):
        """Remove todos os breakpoints."""
        self.breakpoints.clear()
    
    # ==================== LIMPEZA E RESET ====================
    
    def reset(self):
        """Zera toda a memória."""
        self.data = [0] * MEMORY_SIZE
        self.breakpoints.clear()
    
    def clear_range(self, start_address, end_address):
        """Zera intervalo de endereços."""
        start_address = clamp_address(start_address) & 0xFFFF
        end_address = clamp_address(end_address) & 0xFFFF
        
        if start_address <= end_address:
            for addr in range(start_address, end_address + 1):
                self.data[addr] = 0
        else:
            # Wrap-around
            for addr in range(start_address, MEMORY_SIZE):
                self.data[addr] = 0
            for addr in range(0, end_address + 1):
                self.data[addr] = 0
    
    # ==================== ESTATÍSTICAS ====================
    
    def get_non_zero_words(self):
        """Retorna lista de endereços com valores não-zero."""
        return [i for i, val in enumerate(self.data) if val != 0]
    
    def count_non_zero(self):
        """Conta palavras não-zero na memória."""
        return sum(1 for val in self.data if val != 0)
    
    def print_non_zero(self, limit=20):
        """Imprime palavras não-zero até o limite."""
        print("=" * 70)
        print("MEMÓRIA (posições não-zero)")
        print("=" * 70)
        
        count = 0
        for addr, val in enumerate(self.data):
            if val != 0:
                print(f"Mem[{addr:5d}]: 0x{val:08x} (decimal: {val})")
                count += 1
                if count >= limit:
                    remaining = self.count_non_zero() - count
                    if remaining > 0:
                        print(f"... ({remaining} posições omitidas)")
                    break
    
    def dump_memory(self, start=0, count=10):
        """Faz dump de intervalo de memória."""
        start = clamp_address(start) & 0xFFFF
        
        print("=" * 70)
        print(f"DUMP DE MEMÓRIA (de 0x{start:04x})")
        print("=" * 70)
        
        for i in range(count):
            addr = (start + i) & 0xFFFF
            val = self.data[addr]
            print(f"0x{addr:04x}: 0x{val:08x}")
    
    # ==================== DEBUG ====================
    
    def verify_size(self):
        """Verifica integridade da memória."""
        return len(self.data) == MEMORY_SIZE
    
    def get_stats(self):
        """Retorna estatísticas da memória."""
        non_zero = self.count_non_zero()
        return {
            'total_words': MEMORY_SIZE,
            'non_zero_words': non_zero,
            'zero_words': MEMORY_SIZE - non_zero,
            'breakpoints': len(self.breakpoints)
        }
