<h1 align="center" style="font-weight: bold;">
  Simulador Funcional do Processador UFLA-RISC
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/Assembly-UFLA--RISC-black?style=for-the-badge" alt="Assembly">
  <img src="https://img.shields.io/badge/Architecture-32--bit%20RISC-blue?style=for-the-badge" alt="32-bit RISC">
</p>

---

## 📋 Índice

1. [Contexto do Projeto](#1-contexto-do-projeto)
2. [Características do UFLA-RISC](#2-características-do-ufla-risc)
3. [Instalação e Uso](#3-instalação-e-uso)
4. [Arquitetura do Simulador](#4-arquitetura-do-simulador)
5. [Conjunto de Instruções](#5-conjunto-de-instruções)
6. [Formato de Entrada/Saída](#6-formato-de-entradasaída)
7. [Testes](#7-testes)
8. [Estrutura do Projeto](#8-estrutura-do-projeto)
9. [Documentação Técnica](#9-documentação-técnica)
10. [Colaboradores](#10-colaboradores)

---

## 1. CONTEXTO DO PROJETO

Este projeto implementa um **simulador funcional** para o processador didático RISC de 32 bits **UFLA-RISC**. 

### Objetivos
- Fornecer ferramenta para execução, depuração e teste de programas em nível de arquitetura
- Implementar pipeline de 4 estágios (IF, ID, EX/MEM, WB)
- Simular banco de 32 registradores de 32 bits
- Gerenciar memória de 64K palavras (256KB total)
- Suportar conjunto de instruções RISC completo

### Contexto Acadêmico
**Disciplina:** Arquitetura de Computadores II (GCC123/PCC507)  
**Instituição:** Universidade Federal de Lavras (UFLA)  
**Professor:** Luiz Henrique A. Correia  
**Semestre:** 2º/2025

---

## 2. CARACTERÍSTICAS DO UFLA-RISC

### Especificações Técnicas

| Componente | Especificação |
|------------|---------------|
| **Arquitetura** | RISC de 32 bits |
| **Registradores** | 32 registradores de uso geral (R0-R31) |
| **Memória** | 64K palavras de 32 bits (256KB) |
| **Endereçamento** | 16 bits (palavra) |
| **Pipeline** | 4 estágios (IF, ID, EX/MEM, WB) |
| **Flags** | neg, zero, carry, overflow |
| **Instruções** | 30+ instruções (22 básicas + 8+ adicionais) |

### Pipeline de 4 Estágios

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│   IF    │ -> │   ID    │ -> │ EX/MEM  │ -> │   WB    │
│ Fetch   │    │ Decode  │    │ Execute │    │  Write  │
│ Instr.  │    │ & Read  │    │ & Mem   │    │  Back   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

1. **IF (Instruction Fetch):** Busca instrução na memória
2. **ID (Instruction Decode):** Decodifica e lê registradores
3. **EX/MEM (Execute/Memory):** Executa ALU ou acessa memória
4. **WB (Write Back):** Escreve resultado em registrador

**CPI (Cycles Per Instruction):** 4.0 ciclos por instrução

---

## 3. INSTALAÇÃO E USO

### 3.1. Pré-requisitos

- **Python 3.8+** (testado em 3.8, 3.9, 3.10, 3.11)
- Sistema operacional: Windows, Linux ou macOS

### 3.2. Instalação

```bash
# Clone o repositório
git clone https://github.com/MarcoTFranco/ufla-risc-simulador-grupo6-gcc123.git

# Entre no diretório
cd ufla-risc-simulador-grupo6-gcc123
```

### 3.3. Uso Rápido

#### Passo 1: Escrever Código Assembly

Crie um arquivo `.asm` (exemplo: `programa.asm`):

```assembly
# Exemplo: Soma de dois números
address 0
lch r1, 0x0000      # Carrega parte alta
lcl r1, 0x000A      # r1 = 10
lch r2, 0x0000
lcl r2, 0x0014      # r2 = 20
add r3, r1, r2      # r3 = r1 + r2 = 30
store r0, r3        # Armazena resultado em mem[0]
halt                # Para execução
```

#### Passo 2: Montar (Assembly → Binário)

```bash
python src/interpretador/main.py programa.asm binarios/programa.bin
```

**Saída esperada:**
```
Montando 'programa.asm'...
✓ Montagem concluída com sucesso!
✓ Arquivo gerado: binarios/programa.bin
✓ Total de instruções: 7
✓ Total de labels: 0
```

#### Passo 3: Executar no Simulador

**Modo Padrão (apenas resumo):**
```bash
python src/simulador/main.py binarios/programa.bin
```

**Modo Verbose (debug completo):**
```bash
python src/simulador/main.py binarios/programa.bin --verbose
```

**Saída esperada (modo padrão):**
```
Carregando programa: binarios/programa.bin
✓ Programa carregado: 7 instruções

======================================================================
INICIANDO SIMULAÇÃO UFLA-RISC
MODO: SILENCIOSO (apenas resumo final)
======================================================================

======================================================================
SIMULAÇÃO FINALIZADA
======================================================================
Total de ciclos: 28
Total de instruções: 7
CPI (Cycles Per Instruction): 4.00
✓ CPI perfeito! (4 estágios por instrução)

======================================================================
ESTADO FINAL DA CPU
======================================================================
R 1: 0x0000000a (u32:         10, s32:         10)
R 2: 0x00000014 (u32:         20, s32:         20)
R 3: 0x0000001e (u32:         30, s32:         30)
```

---

## 4. ARQUITETURA DO SIMULADOR

### 4.1. Componentes Principais

```
┌───────────────────────────────────────────────────────────┐
│                    UFLA-RISC SIMULATOR                    │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────┐    │
│  │   Memory    │<-->│   CPU State  │<-->│    ALU     │    │
│  │   64K x 32  │    │  32 Regs + PC│    │  + Flags   │    │
│  └─────────────┘    └──────────────┘    └────────────┘    │
│         ↑                   ↑                   ↑         │
│         │                   │                   │         │
│         └───────────────────┴───────────────────┘         │
│                             |                             │
│                   ┌─────────┴──────────┐                  │
│                   │  Control Unit      │                  │
│                   │  (Branch/Jump)     │                  │
│                   └────────────────────┘                  │
│                             |                             │
│                   ┌─────────┴──────────┐                  │
│                   │ Instruction Decoder│                  │
│                   └────────────────────┘                  │
└───────────────────────────────────────────────────────────┘
```

### 4.2. Módulos do Código

| Arquivo | Responsabilidade |
|---------|------------------|
| `cpu_state.py` | Gerencia registradores, PC, IR e flags |
| `memory.py` | Implementa memória de 64K palavras |
| `alu.py` | Operações aritméticas e lógicas |
| `control_unit.py` | Controle de fluxo (branches, jumps) |
| `instruction_decoder.py` | Decodifica instruções de 32 bits |
| `simulator.py` | Orquestra pipeline e execução |
| `utils.py` | Funções auxiliares de conversão |

---

## 5. CONJUNTO DE INSTRUÇÕES

### 5.1. Instruções Básicas (22 obrigatórias)

#### Operações Aritméticas e Lógicas

| Mnemônico | Opcode | Formato | Operação | Flags |
|-----------|--------|---------|----------|-------|
| `add` | 0x01 | `add rc, ra, rb` | rc = ra + rb | N Z C V |
| `sub` | 0x02 | `sub rc, ra, rb` | rc = ra - rb | N Z C V |
| `xor` | 0x04 | `xor rc, ra, rb` | rc = ra ^ rb | N Z |
| `or` | 0x05 | `or rc, ra, rb` | rc = ra \| rb | N Z |
| `and` | 0x07 | `and rc, ra, rb` | rc = ra & rb | N Z |
| `passnota` | 0x06 | `passnota rc, ra` | rc = ~ra | N Z |
| `zeros` | 0x03 | `zeros rc` | rc = 0 | Z |
| `passa` | 0x0C | `passa rc, ra` | rc = ra | N Z |

#### Operações de Shift

| Mnemônico | Opcode | Operação | Flags |
|-----------|--------|----------|-------|
| `asl` | 0x08 | Shift aritmético esquerda | N Z |
| `asr` | 0x09 | Shift aritmético direita | N Z |
| `lsl` | 0x0A | Shift lógico esquerda | N Z |
| `lsr` | 0x0B | Shift lógico direita | N Z |

#### Memória e Constantes

| Mnemônico | Opcode | Operação | Descrição |
|-----------|--------|----------|-----------|
| `lch` | 0x0E | rc[31:16] = const16 | Carrega 16 bits altos |
| `lcl` | 0x0F | rc[15:0] = const16 | Carrega 16 bits baixos |
| `load` | 0x10 | rc = mem[ra] | Carrega da memória |
| `store` | 0x11 | mem[rc] = ra | Armazena na memória |

#### Controle de Fluxo

| Mnemônico | Opcode | Operação | Descrição |
|-----------|--------|----------|-----------|
| `jal` | 0x12 | r31=PC; PC=end | Jump and link |
| `jr` | 0x13 | PC = rc | Jump register |
| `beq` | 0x14 | if (ra==rb) PC=end | Branch se igual |
| `bne` | 0x15 | if (ra!=rb) PC=end | Branch se diferente |
| `j` | 0x16 | PC = end | Jump incondicional |

#### Especial

| Mnemônico | Opcode | Operação |
|-----------|--------|----------|
| `halt` | 0xFF | Para execução |

---

### 5.2. Instruções Adicionais (8+ do Grupo)

| Mnemônico | Opcode | Formato | Operação | Justificativa |
|-----------|--------|---------|----------|---------------|
| `slt` | 0x17 | `slt rc, ra, rb` | rc = (ra < rb) ? 1 : 0 | Comparação para loops |
| `mul` | 0x18 | `mul rc, ra, rb` | rc = ra * rb | Multiplicação eficiente |
| `div` | 0x19 | `div rc, ra, rb` | rc = ra / rb | Divisão inteira |
| `mod` | 0x1A | `mod rc, ra, rb` | rc = ra % rb | Resto da divisão |
| `neg` | 0x1B | `neg rc, ra` | rc = -ra | Negação aritmética |
| `inc` | 0x1C | `inc rc, ra` | rc = ra + 1 | Incremento |
| `dec` | 0x1D | `dec rc, ra` | rc = ra - 1 | Decremento |
| `nop` | 0x1E | `nop` | Nenhuma operação | Alinhamento de código |

---

## 6. FORMATO DE ENTRADA/SAÍDA

### 6.1. Formato do Arquivo Assembly (.asm)

```assembly
# Comentários começam com '#' ou ';'

# Diretiva de endereço (opcional)
address 0

# Instruções
add r3, r1, r2      # Soma r1 + r2 → r3
store r0, r3        # Armazena r3 em mem[r0]

# Labels para branches/jumps
loop:
    beq r1, r2, fim
    add r1, r1, r2
    j loop

fim:
    halt
```

### 6.2. Formato do Arquivo Binário (.bin)

```
address 0000000000000000
00000001000000010000001000000011
00010001000000000000001100000000
00010100000000010000001000000101
00000001000000010000001000000001
00010110000000000000000000000010
11111111111111111111111111111111
```

**Regras:**
- Uma instrução por linha (32 bits em binário)
- `address <endereço_binário_16bits>` define posição inicial
- Se omitir `address`, começa em endereço 0

### 6.3. Formato de Saída do Simulador

#### Modo Padrão (Resumo)
```
Total de ciclos: 28
Total de instruções: 7
CPI: 4.00

ESTADO FINAL DA CPU
R 1: 0x0000000a (u32: 10, s32: 10)
R 3: 0x0000001e (u32: 30, s32: 30)
```

#### Modo Verbose (Ciclo a Ciclo)
```
======================================================================
CICLO 1 - Estágio: IF
Instrução #1
======================================================================
IR <- 0x0e010000
PC <- 1 (0x0001)
Instrução: LCH      R1, 0x0000

======================================================================
CICLO 2 - Estágio: ID
Instrução #1
======================================================================
Decodificação da instrução
Opcode: 0x0e (LCH)
Operandos lidos:
  RA (R1) = 0x00000000
(Sem alterações em registradores/memória)

[... continua para EX/MEM e WB ...]
```

---

## 7. TESTES

### 7.1. Programas de Teste Disponíveis

| Arquivo | Descrição | Instruções Testadas |
|---------|-----------|---------------------|
| `01_teste_add.asm` | Soma básica | ADD, LCH, LCL |
| `02_teste_sub.asm` | Subtração | SUB, flags negativos |
| `03_teste_logicas.asm` | Operações lógicas | XOR, OR, AND, NOT |
| `04_teste_shifts.asm` | Shifts | ASL, ASR, LSL, LSR |
| `05_teste_memory.asm` | Memória | LOAD, STORE |
| `06_teste_branches.asm` | Branches | BEQ, BNE |
| `07_teste_jumps.asm` | Jumps | JAL, JR, J |
| `08_teste_adicionais.asm` | Novas instruções | MUL, DIV, MOD, etc |
| `09_fatorial.asm` | Fatorial recursivo | Programa completo |
| `10_fibonacci.asm` | Fibonacci | Loop e recursão |
| `11_soma_vetor.asm` | Soma de vetor | Loops e memória |

### 7.2. Executar Teste Individual

```bash
# Montar
python src/interpretador/main.py exemplos/09_fatorial.asm binarios/09_fatorial.bin

# Executar
python src/simulador/main.py binarios/09_fatorial.bin --verbose
```

### 7.3. Validação de Resultados

✅ **Critérios de Sucesso:**
- CPI = 4.00 (exato)
- Flags corretos após cada operação
- Memória e registradores com valores esperados
- Sem erros de execução

---

## 8. ESTRUTURA DO PROJETO

```
ufla-risc-simulador-grupo6-gcc123/
│
├── binarios/                      # Arquivos .bin gerados
│   └── (gerados após montagem)
│
├── docs/                          # Documentação técnica
│   ├── manual_tecnico.pdf         # Manual completo
│   ├── instrucoes_adicionais.md   # Justificativas
│   └── tutorial_uso.md            # Tutorial detalhado
│
├── exemplos/                      # Programas .asm de teste
│   ├── 01_teste_add.asm
│   ├── 02_teste_sub.asm
│   ├── 03_teste_logicas.asm
│   ├── 04_teste_shifts.asm
│   ├── 05_teste_memory.asm
│   ├── 06_teste_branches.asm
│   ├── 07_teste_jumps.asm
│   ├── 08_teste_adicionais.asm
│   ├── 09_fatorial.asm
│   ├── 10_fibonacci.asm
│   └── 11_soma_vetor.asm
│
├── src/
│   ├── interpretador/             # Módulo Assembler
│   │   ├── assembler.py           # Orquestra montagem
│   │   ├── encoder.py             # Codifica instruções
│   │   ├── main.py                # CLI do assembler
│   │   ├── opcodes.py             # Tabela de opcodes
│   │   └── parser.py              # Parser de assembly
│   │
│   └── simulador/                 # Módulo Simulador
│       ├── alu.py                 # Unidade aritmética
│       ├── control_unit.py        # Controle de fluxo
│       ├── cpu_state.py           # Estado da CPU
│       ├── instruction_decoder.py # Decodificador
│       ├── main.py                # CLI do simulador
│       ├── memory.py              # Memória 64K
│       ├── simulator.py           # Pipeline principal
│       └── utils.py               # Funções auxiliares
│
├── .gitignore
└── README.md
```

---

## 9. DOCUMENTAÇÃO TÉCNICA

### 9.1. Documentos Disponíveis

📄 **[Manual Técnico (PDF)](docs/manual_tecnico.pdf)**  
Documentação completa do projeto incluindo:
- Decisões de implementação
- Descrição detalhada de todas as instruções
- Análise de testes realizados
- Diagramas de hardware

📝 **[Instruções Adicionais](docs/instrucoes_adicionais.md)**  
Justificativa técnica das 8+ instruções implementadas pelo grupo

📖 **[Tutorial de Uso](docs/tutorial_uso.md)**  
Guia passo a passo para iniciantes

### 9.2. Decisões de Implementação

#### Pipeline
- Escolhemos pipeline de 4 estágios (ao invés de 5) para simplificar controle
- Estágios EX e MEM foram combinados pois operações de memória são simples

#### Flags
- Implementados 4 flags: neg, zero, carry, overflow
- Atualizados apenas em operações ALU (não em loads/stores)
- Flags de carry/overflow zerados em operações lógicas

#### Memória
- Endereçamento por palavra (não por byte)
- 64K palavras = 256KB total
- Sem cache (simulador funcional)

---

## 10. COLABORADORES

<table>
  <tr>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/134017049?v=4" width="100px;" alt="Clarisse Lacerda Pimentel"/>
        <br />
        <sub><b>Clarisse Lacerda Pimentel</b></sub>
      </a>
      <br />
      <sub>Assembler + Documentação</sub>
    </td>
    <td align="center">
      <a href="https://github.com/Clofender">
        <img src="https://avatars.githubusercontent.com/u/73314533?v=4" width="100px;" alt="Daniel Silva Ferraz Neto"/>
        <br />
        <sub><b>Daniel Silva Ferraz Neto</b></sub>
      </a>
      <br />
      <sub>ALU + Operações</sub>
    </td>
    <td align="center">
      <a href="#">
        <img src="https://avatars.githubusercontent.com/u/10137?v=4" width="100px;" alt="Helder Jose Avila"/>
        <br />
        <sub><b>Helder Jose Avila</b></sub>
      </a>
      <br />
      <sub>Controle + Memória</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/zector1">
        <img src="https://avatars.githubusercontent.com/u/137319815?v=4" width="100px;" alt="José Victor Miranda de Oliveira"/>
        <br />
        <sub><b>José Victor Miranda de Oliveira</b></sub>
      </a>
      <br />
      <sub>Pipeline + Simulador</sub>
    </td>
    <td align="center">
      <a href="https://github.com/MarcoTFranco">
        <img src="https://avatars.githubusercontent.com/u/121970508?v=4" width="100px;" alt="Marco Tulio Franco Silva"/>
        <br />
        <sub><b>Marco Tulio Franco Silva</b></sub>
      </a>
      <br />
      <sub>Testes + Integração</sub>
    </td>
  </tr>
</table>

---

## 📚 Referências

- PATTERSON, David A.; HENNESSY, John L. **Computer Organization and Design: The Hardware/Software Interface**. 5th ed. Morgan Kaufmann, 2014.
- HARRIS, Sarah L.; HARRIS, David M. **Digital Design and Computer Architecture**. 2nd ed. Morgan Kaufmann, 2012.
- Material didático da disciplina GCC123/PCC507 - UFLA

---

## 📄 Licença

Este é um projeto **estritamente acadêmico** desenvolvido para a disciplina de Arquitetura de Computadores II da UFLA. 

**Sem licença para uso comercial.**

---

## 🤝 Contribuindo

Este é um projeto acadêmico fechado. Contribuições externas não são aceitas neste momento.

Para dúvidas ou sugestões, entre em contato com os colaboradores.

---

## 📞 Contato

**Instituição:** Universidade Federal de Lavras (UFLA)  
**Departamento:** Ciência da Computação  
**Disciplina:** GCC123/PCC507 - Arquitetura de Computadores II  
**Professor:** Luiz Henrique A. Correia

---

<p align="center">
  Desenvolvido com 💙 por estudantes de Ciência da Computação da UFLA
</p>

<p align="center">
  <sub>Último update: Novembro 2025</sub>
</p>