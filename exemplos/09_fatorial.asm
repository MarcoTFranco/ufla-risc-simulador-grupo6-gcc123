# Programa: Fatorial de 5
# Descrição: Calcula 5! = 120

lcl r1, 5                # n = 5
lcl r2, 1                # resultado = 1
lcl r3, 1                # contador = 1

loop:
slt r4, r3, r1           # r4 = (contador < n)
beq r4, r0, fim          # Se r4 == 0, termina

mul r2, r2, r3           # resultado *= contador
inc r3, r3               # contador++
j loop

fim:
# r2 deve conter 120
halt
