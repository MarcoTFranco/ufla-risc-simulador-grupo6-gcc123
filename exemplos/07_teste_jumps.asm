# Teste: JAL, JR, J
# Descrição: Valida jumps incondicionais

# Teste J (jump incondicional)
j pula_inicio

lcl r1, 999              # Não deve executar

pula_inicio:
lcl r1, 1                # r1 = 1

# Teste JAL (jump and link)
jal funcao
lcl r2, 2                # r2 = 2 (após retorno)
j fim

funcao:
lcl r3, 3                # r3 = 3
jr r31                   # Retorna (JR)

fim:
halt
