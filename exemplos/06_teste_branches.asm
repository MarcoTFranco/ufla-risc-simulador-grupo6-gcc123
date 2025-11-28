# Teste: BEQ e BNE
# Descrição: Valida desvios condicionais

# Teste BEQ (branch tomado)
lcl r1, 10
lcl r2, 10
beq r1, r2, igual        # Deve desviar para 'igual'
lcl r3, 1                # Não deve executar

igual:
lcl r3, 100              # r3 = 100

# Teste BNE (branch tomado)
lcl r4, 5
lcl r5, 10
bne r4, r5, diferente    # Deve desviar para 'diferente'
lcl r6, 1                # Não deve executar

diferente:
lcl r6, 200              # r6 = 200

halt