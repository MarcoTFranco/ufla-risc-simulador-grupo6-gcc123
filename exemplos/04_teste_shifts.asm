# Teste: Instruções de Shift
# Descrição: Testa ASL, ASR, LSL, LSR

# Teste ASL: 0x00000001 << 4 = 0x00000010
lcl r1, 1
lcl r2, 4
asl r3, r1, r2           # r3 = 16

# Teste ASR: 0x80000000 >> 1 = 0xC0000000 (aritmético)
lch r4, 0x8000
lcl r5, 1
asr r6, r4, r5           # r6 = 0xC0000000

# Teste LSL: 0x00000002 << 3 = 0x00000010
lcl r7, 2
lcl r8, 3
lsl r9, r7, r8           # r9 = 16

# Teste LSR: 0x80000000 >> 1 = 0x40000000 (lógico)
lch r10, 0x8000
lcl r11, 1
lsr r12, r10, r11        # r12 = 0x40000000

halt
