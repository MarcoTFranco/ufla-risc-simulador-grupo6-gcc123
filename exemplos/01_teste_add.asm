# Teste: Instrução ADD
# Descrição: Testa adição básica e flags

# Teste 1: Soma simples (5 + 10 = 15)
lcl r1, 5
lcl r2, 10
add r3, r1, r2           # r3 deve ser 15

# Teste 2: Soma com zero (15 + 0 = 15)
zeros r4
add r5, r3, r4           # r5 deve ser 15

# Teste 3: Overflow positivo (MAX + 1)
lch r6, 0x7FFF
lcl r6, 0xFFFF          # r6 = 0x7FFFFFFF (MAX_INT)
lcl r7, 1
add r8, r6, r7           # r8 = 0x80000000 (overflow)

halt
