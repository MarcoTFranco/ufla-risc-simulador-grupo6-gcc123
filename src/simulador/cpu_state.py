"""
cpu_state.py - Gerenciamento do Estado da CPU

Encapsula o estado interno da CPU (registradores, flags, PC, IR)
e fornece operações para leitura/escrita segura.
"""

from utils import (MASK32, NUM_REGISTERS, clamp_register, create_flags_dict,
                   flags_to_string, is_valid_register, to_s32, to_u32)


class CPUState:
    """Representa o estado completo da CPU UFLA-RISC."""

    def __init__(self):
        """Inicializa CPU com estado zerado."""
        self.regs = [0] * NUM_REGISTERS
        self.PC = 0
        self.IR = 0
        self.neg = 0
        self.zero = 0
        self.carry = 0
        self.overflow = 0

    # ==================== REGISTRADORES ====================

    def read_register(self, reg_idx):
        """Lê valor de registrador."""
        reg_idx = clamp_register(reg_idx)
        return self.regs[reg_idx]

    def write_register(self, reg_idx, value):
        """Escreve valor em registrador (R0 sempre permanece 0)."""
        reg_idx = clamp_register(reg_idx)
        value = to_u32(value)

        if reg_idx != 0:  # R0 é sempre 0
            self.regs[reg_idx] = value

    def read_register_signed(self, reg_idx):
        """Lê valor de registrador como inteiro com sinal."""
        return to_s32(self.read_register(reg_idx))

    # ==================== PROGRAM COUNTER ====================

    def increment_pc(self):
        """Incrementa PC (sem carry para memória)."""
        self.PC = to_u32(self.PC + 1)

    def set_pc(self, value):
        """Define novo valor para PC."""
        self.PC = to_u32(value)

    def get_pc(self):
        """Retorna valor atual de PC."""
        return self.PC

    # ==================== INSTRUCTION REGISTER ====================

    def set_ir(self, instruction):
        """Define nova instrução em IR."""
        self.IR = to_u32(instruction)

    def get_ir(self):
        """Retorna instrução atual em IR."""
        return self.IR

    # ==================== FLAGS ====================

    def set_flags(self, neg=None, zero=None, carry=None, overflow=None):
        """Atualiza flags seletivamente."""
        if neg is not None:
            self.neg = 1 if neg else 0
        if zero is not None:
            self.zero = 1 if zero else 0
        if carry is not None:
            self.carry = 1 if carry else 0
        if overflow is not None:
            self.overflow = 1 if overflow else 0

    def clear_flags(self):
        """Zera todos os flags."""
        self.neg = self.zero = self.carry = self.overflow = 0

    def get_flags_dict(self):
        """Retorna flags como dicionário."""
        return create_flags_dict(self.neg, self.zero, self.carry, self.overflow)

    def get_flags_string(self):
        """Retorna flags como string legível."""
        return flags_to_string(self.get_flags_dict())

    # ==================== ESTADO COMPLETO ====================

    def snapshot(self):
        """Captura snapshot do estado atual para comparação."""
        return {
            'regs': list(self.regs),
            'pc': self.PC,
            'ir': self.IR,
            'flags': self.get_flags_dict()
        }

    def compare_with(self, other_snapshot):
        """
        Compara estado atual com snapshot anterior.
        Retorna dicionário com diferenças.
        """
        changes = {
            'registers': [],
            'pc_changed': False,
            'ir_changed': False,
            'flags_changed': {}
        }

        # Verificar registradores
        for i in range(NUM_REGISTERS):
            if self.regs[i] != other_snapshot['regs'][i]:
                changes['registers'].append({
                    'index': i,
                    'old': other_snapshot['regs'][i],
                    'new': self.regs[i]
                })

        # Verificar PC
        if self.PC != other_snapshot['pc']:
            changes['pc_changed'] = True
            changes['pc_old'] = other_snapshot['pc']
            changes['pc_new'] = self.PC

        # Verificar IR
        if self.IR != other_snapshot['ir']:
            changes['ir_changed'] = True
            changes['ir_old'] = other_snapshot['ir']
            changes['ir_new'] = self.IR

        # Verificar flags
        current_flags = self.get_flags_dict()
        for flag_name in ['neg', 'zero', 'carry', 'overflow']:
            if current_flags[flag_name] != other_snapshot['flags'][flag_name]:
                changes['flags_changed'][flag_name] = {
                    'old': other_snapshot['flags'][flag_name],
                    'new': current_flags[flag_name]
                }

        return changes

    def reset(self):
        """Reseta CPU para estado inicial."""
        self.regs = [0] * NUM_REGISTERS
        self.PC = 0
        self.IR = 0
        self.clear_flags()

    # ==================== EXIBIÇÃO ====================

    def print_registers(self, show_zero=False):
        """Imprime todos os registradores."""
        print("=" * 70)
        print("REGISTRADORES")
        print("=" * 70)
        for i in range(NUM_REGISTERS):
            if self.regs[i] != 0 or show_zero:
                val_u32 = self.regs[i]
                val_s32 = to_s32(val_u32)
                print(
                    f"R{i:2d}: 0x{val_u32:08x} (u32: {val_u32:10d}, s32: {val_s32:10d})")

    def print_state(self):
        """Imprime estado completo da CPU."""
        print("=" * 70)
        print("ESTADO DA CPU")
        print("=" * 70)
        print(f"PC: {self.PC} (0x{self.PC:04x})")
        print(f"IR: {hex(self.IR)} (binary: {bin(self.IR)})")
        print(f"Flags: {self.get_flags_string()}")
        self.print_registers(show_zero=False)


# ==================== FUNÇÕES AUXILIARES ====================
def compare_states(state1, state2):
    """Compara dois snapshots de estado."""
    diffs = {
        'registers': [],
        'pc_diff': state1['pc'] != state2['pc'],
        'ir_diff': state1['ir'] != state2['ir'],
        'flags_diff': {}
    }

    for i in range(NUM_REGISTERS):
        if state1['regs'][i] != state2['regs'][i]:
            diffs['registers'].append(
                (i, state1['regs'][i], state2['regs'][i]))

    for flag in ['neg', 'zero', 'carry', 'overflow']:
        if state1['flags'][flag] != state2['flags'][flag]:
            diffs['flags_diff'][flag] = (
                state1['flags'][flag], state2['flags'][flag])

    return diffs
