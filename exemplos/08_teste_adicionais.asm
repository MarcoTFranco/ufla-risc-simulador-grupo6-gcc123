# Teste: Instruções Adicionais (MUL, DIV, MOD, SLT, INC, DEC, NEG)

# Teste MUL: 5 * 7 = 35
lcl r1, 5
lcl r2, 7
mul r3, r1, r2           # r3 = 35

# Teste DIV: 20 / 4 = 5
lcl r4, 20
lcl r5, 4
div r6, r4, r5           # r6 = 5

# Teste MOD: 23 % 5 = 3
lcl r7, 23
lcl r8, 5
mod r9, r7, r8           # r9 = 3

# Teste SLT: 5 < 10 = 1
lcl r10, 5
lcl r11, 10
slt r12, r10, r11        # r12 = 1

# Teste INC: 10 + 1 = 11
lcl r13, 10
inc r14, r13             # r14 = 11

# Teste DEC: 10 - 1 = 9
dec r15, r13             # r15 = 9

# Teste NEG: -10
neg r16, r13             # r16 = -10

# Teste NOP
nop

halt
