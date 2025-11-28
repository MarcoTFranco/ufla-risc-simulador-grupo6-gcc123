# teste_completo_v2.asm - Teste Abrangente do UFLA-RISC (CORRIGIDO)
# Testa todas as correções implementadas

# ============================================================
# TESTE 1: OPERAÇÕES ARITMÉTICAS E FLAGS (EX/MEM)
# ============================================================
address 0

# Teste ADD com flags
lcl r1, 10          # R1 = 10
lcl r2, 5           # R2 = 5
add r3, r1, r2      # R3 = 15, flags devem ser atualizados em EX/MEM
                    # neg=0, zero=0, carry=0, overflow=0

# Teste SUB com flags
sub r4, r1, r2      # R4 = 5
                    # neg=0, zero=0, carry=0, overflow=0

# Teste ZEROS (sem parâmetro)
zeros r5            # R5 = 0
                    # neg=0, zero=1, carry=0, overflow=0

# ============================================================
# TESTE 2: OPERAÇÕES LÓGICAS
# ============================================================

lcl r6, 15          # R6 = 0x0F (0000 1111)
lcl r7, 51          # R7 = 0x33 (0011 0011)

xor r8, r6, r7      # R8 = 0x3C (0011 1100)
or r9, r6, r7       # R9 = 0x3F (0011 1111)
and r10, r6, r7     # R10 = 0x03 (0000 0011)
passnota r11, r6    # R11 = ~R6 = 0xFFFFFFF0

# ============================================================
# TESTE 3: SHIFTS
# ============================================================

lcl r12, 4          # R12 = 4
lcl r13, 2          # R13 = 2 (shift amount)

asl r14, r12, r13   # R14 = 4 << 2 = 16
asr r15, r12, r13   # R15 = 4 >> 2 = 1 (aritmético)
lsl r16, r12, r13   # R16 = 4 << 2 = 16
lsr r17, r12, r13   # R17 = 4 >> 2 = 1 (lógico)

# ============================================================
# TESTE 4: INC/DEC (2 REGISTRADORES)
# ============================================================

lcl r18, 100        # R18 = 100
inc r19, r18        # R19 = 101 (R18 + 1)
dec r20, r18        # R20 = 99 (R18 - 1)

# ============================================================
# TESTE 5: MULTIPLICAÇÃO, DIVISÃO, MÓDULO
# ============================================================

lcl r21, 12         # R21 = 12
lcl r22, 5          # R22 = 5

mul r23, r21, r22   # R23 = 60
div r24, r21, r22   # R24 = 2 (12 / 5)
mod r25, r21, r22   # R25 = 2 (12 % 5)

# ============================================================
# TESTE 6: MEMÓRIA (LOAD/STORE)
# ============================================================

# Armazenar valor na memória
lcl r26, 200        # R26 = 200 (endereço)
lcl r27, 42         # R27 = 42 (valor)
store r26, r27      # Mem[200] = 42

# Carregar valor da memória
load r28, r26       # R28 = Mem[200] = 42

# ============================================================
# TESTE 7: BRANCHES (VALIDAÇÃO 8 BITS)
# ============================================================

lcl r29, 10         # R29 = 10
lcl r30, 10         # R30 = 10

# CORRIGIDO: BEQ agora pula para label, não endereço direto
beq r29, r30, skip_section  # Se R29 == R30, pula para skip_section

# Esta linha NÃO será executada se branch for tomado
lcl r1, 999

skip_section:
# ============================================================
# TESTE 8: JAL/JR (CHAMADA DE PROCEDIMENTO)
# ============================================================

jal proc_teste      # Chama procedimento
                    # R31 = endereço de retorno

# Retorno do procedimento
lcl r2, 55          # R2 = 55 (código executado após retorno)

# Teste com BNE (branch NOT taken)
lcl r29, 10
lcl r30, 20
bne r29, r30, never_taken  # Pula se diferentes (vai pular)

lcl r31, 88         # Esta linha SERÁ executada

never_taken:
    lcl r1, 999     # Esta linha NÃO será executada

halt                # Fim do programa

# ============================================================
# PROCEDIMENTO DE TESTE
# ============================================================

proc_teste:
    lcl r3, 777     # R3 = 777 (dentro do procedimento)
    jr r31          # Retorna para endereço em R31

# ============================================================
# RESULTADO ESPERADO APÓS EXECUÇÃO:
# ============================================================
# R1 = 10 (não foi sobrescrito)
# R2 = 55
# R3 = 777
# R4 = 5
# R5 = 0
# R6 = 15
# R7 = 51
# R8 = 60
# R9 = 63
# R10 = 3
# R11 = 0xFFFFFFF0
# R12 = 4
# R13 = 2
# R14 = 16
# R15 = 1
# R16 = 16
# R17 = 1
# R18 = 100
# R19 = 101
# R20 = 99
# R21 = 12
# R22 = 5
# R23 = 60
# R24 = 2
# R25 = 2
# R26 = 200
# R27 = 42
# R28 = 42
# R29 = 10
# R30 = 20
# R31 = endereço de retorno
# Mem[200] = 42
# Flags: depende da última operação
# CPI: 4.0 (perfeito)