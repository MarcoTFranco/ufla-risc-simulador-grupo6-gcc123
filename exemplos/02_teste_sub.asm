# Teste: Instrução SUB
# Descrição: Testa subtração e flags

# Teste 1: Subtração simples (20 - 5 = 15)
lcl r1, 20
lcl r2, 5
sub r3, r1, r2           # r3 deve ser 15

# Teste 2: Resultado zero (10 - 10 = 0)
lcl r4, 10
sub r5, r4, r4           # r5 = 0, flag zero = 1

# Teste 3: Resultado negativo (5 - 10)
lcl r6, 5
lcl r7, 10
sub r8, r6, r7           # r8 deve ser negativo

halt
