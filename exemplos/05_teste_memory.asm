# Teste: LOAD e STORE
# Descrição: Valida acesso à memória

# Preparar endereços
lcl r1, 100              # Endereço de memória
lcl r2, 42               # Valor a armazenar

# STORE: Mem[100] = 42
store r1, r2

# LOAD: r3 = Mem[100]
load r3, r1              # r3 deve ser 42

# Teste com outro endereço
lcl r4, 200
lcl r5, 99
store r4, r5
load r6, r4              # r6 deve ser 99

halt
