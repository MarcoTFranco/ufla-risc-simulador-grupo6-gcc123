"""
utils.py - Utilitários e Constantes Globais

Fornece funções de conversão entre representações numéricas,
máscaras de bits e funções de formatação para o simulador.
"""

# ==================== CONSTANTES ====================

MASK32 = 0xFFFFFFFF
MASK16 = 0xFFFF
MASK8 = 0xFF
SIGN_BIT_32 = 0x80000000

# Tamanho da memória (64K palavras de 32 bits)
MEMORY_SIZE = 65536

# Número de registradores
NUM_REGISTERS = 32

# ==================== CONVERSÕES ====================


def to_u32(x):
    """Converte número para unsigned 32-bit."""
    return x & MASK32


def to_s32(x):
    """Converte unsigned 32-bit para signed 32-bit (two's complement)."""
    x = x & MASK32
    return x if x < SIGN_BIT_32 else x - 0x100000000


def u32_to_s32(x):
    """Alias para to_s32 (explícito)."""
    return to_s32(x)


def s32_to_u32(x):
    """Converte signed 32-bit para unsigned 32-bit."""
    return to_u32(x)


def extract_bits(value, start, end):
    """
    Extrai bits de 'value' entre posições start:end (inclusive).

    Exemplo: extract_bits(0xFF, 0, 3) retorna bits [0:4]
    """
    mask = ((1 << (end - start + 1)) - 1)
    return (value >> start) & mask


def set_bits(value, start, end, new_bits):
    """
    Define bits em 'value' entre posições start:end para 'new_bits'.

    Retorna o valor modificado.
    """
    mask = ((1 << (end - start + 1)) - 1)
    cleared = value & ~(mask << start)
    return cleared | ((new_bits & mask) << start)


# ==================== FORMATAÇÃO ====================

def hex_format(value, width=8):
    """Formata valor como hexadecimal com padding."""
    return f"0x{value & MASK32:0{width}x}"


def bin_format(value, width=32):
    """Formata valor como binário com padding."""
    return f"0b{value & MASK32:0{width}b}"


def format_register_value(value):
    """Formata valor de registrador em múltiplos formatos."""
    u32_val = value & MASK32
    s32_val = to_s32(u32_val)
    return {
        'hex': hex_format(u32_val),
        'decimal_u': u32_val,
        'decimal_s': s32_val,
        'binary': bin_format(u32_val)
    }


def format_instruction(ir):
    """Formata instrução com seus componentes."""
    return {
        'hex': hex_format(ir),
        'binary': bin_format(ir),
        'opcode': (ir >> 24) & MASK8,
        'ra': (ir >> 16) & MASK8,
        'rb': (ir >> 8) & MASK8,
        'rc': ir & MASK8
    }


# ==================== VALIDAÇÕES ====================

def is_valid_register(reg_idx):
    """Verifica se índice de registrador é válido."""
    return 0 <= reg_idx < NUM_REGISTERS


def clamp_register(reg_idx):
    """Garante que índice está dentro do intervalo válido."""
    return max(0, min(reg_idx, NUM_REGISTERS - 1))


def is_valid_address(addr):
    """Verifica se endereço de memória é válido."""
    return 0 <= addr < MEMORY_SIZE


def clamp_address(addr):
    """Garante que endereço está dentro do intervalo válido."""
    return addr & 0xFFFF  # 16 bits = 64K


# ==================== FLAGS ====================

def get_flag_name(flag_idx):
    """Retorna nome do flag pelo índice."""
    flags = {0: 'neg', 1: 'zero', 2: 'carry', 3: 'overflow'}
    return flags.get(flag_idx, 'unknown')


def create_flags_dict(neg=0, zero=0, carry=0, overflow=0):
    """Cria dicionário com flags."""
    return {
        'neg': neg,
        'zero': zero,
        'carry': carry,
        'overflow': overflow
    }


def flags_to_string(flags_dict):
    """Converte flags para string legível."""
    return (f"neg={flags_dict['neg']} zero={flags_dict['zero']} "
            f"carry={flags_dict['carry']} overflow={flags_dict['overflow']}")


# ==================== UTILIDADES ====================

def popcount(value):
    """Conta número de bits 1 no valor."""
    return bin(value & MASK32).count('1')


def leading_zeros(value):
    """Conta zeros à esquerda em valor de 32 bits."""
    value = value & MASK32
    if value == 0:
        return 32
    return 31 - (value.bit_length() - 1)


def rotl32(value, shift):
    """Rotação left de 32 bits."""
    shift = shift % 32
    return to_u32((value << shift) | (value >> (32 - shift)))


def rotr32(value, shift):
    """Rotação right de 32 bits."""
    shift = shift % 32
    return to_u32((value >> shift) | (value << (32 - shift)))


# ==================== DEBUGGING ====================

def compare_states(state1, state2, verbose=False):
    """
    Compara dois estados e retorna diferenças.

    Retorna lista de tuplas (campo, valor1, valor2).
    """
    diffs = []

    # Comparar registradores
    for i in range(NUM_REGISTERS):
        if state1['regs'][i] != state2['regs'][i]:
            diffs.append(('regs', i, state1['regs'][i], state2['regs'][i]))

    # Comparar PC
    if state1['pc'] != state2['pc']:
        diffs.append(('pc', None, state1['pc'], state2['pc']))

    # Comparar IR
    if state1['ir'] != state2['ir']:
        diffs.append(('ir', None, state1['ir'], state2['ir']))

    # Comparar flags
    for flag in ['neg', 'zero', 'carry', 'overflow']:
        if state1['flags'][flag] != state2['flags'][flag]:
            diffs.append(
                ('flag', flag, state1['flags'][flag], state2['flags'][flag]))

    if verbose:
        for diff in diffs:
            print(f"  Diferença em {diff[0]}: {diff[2]} -> {diff[3]}")

    return diffs
