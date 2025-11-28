# Teste: Instruções Lógicas (AND, OR, XOR, NOT)
# Descrição: Valida operações bit a bit

# Teste AND: 0xFF & 0xF0 = 0xF0
lcl r1, 0xFF
lcl r2, 0xF0
and r3, r1, r2           # r3 = 0xF0

# Teste OR: 0x0F | 0xF0 = 0xFF
lcl r4, 0x0F
lcl r5, 0xF0
or r6, r4, r5            # r6 = 0xFF

# Teste XOR: 0xFF ^ 0xAA = 0x55
lcl r7, 0xFF
lcl r8, 0xAA
xor r9, r7, r8           # r9 = 0x55

# Teste NOT: ~0xFFFF0000 = 0x0000FFFF
lch r10, 0xFFFF
passnota r11, r10        # r11 = 0x0000FFFF

halt