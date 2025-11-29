# Programa: Fibonacci até F(10)
# Descrição: Calcula sequência de Fibonacci

lcl r1, 0                # fib(0) = 0
lcl r2, 1                # fib(1) = 1
lcl r3, 10               # n = 10
lcl r4, 2                # contador = 2

loop:
slt r5, r4, r3           # r5 = (contador < n)
beq r5, r0, fim          # Se r5 == 0, termina

add r6, r1, r2           # fib(i) = fib(i-1) + fib(i-2)
passa r1, r2             # fib(i-2) = fib(i-1)
passa r2, r6             # fib(i-1) = fib(i)

inc r4, r4               # contador++
j loop

fim:
# r2 deve conter F(10) = 55
halt
