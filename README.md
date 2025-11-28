<h1 align="center" style="font-weight: bold;">
  Simulador Funcional do Processador UFLA-RISC
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/Assembly-UFLA--RISC-black?style=for-the-badge" alt="Assembly">
</p>

## 1. CONTEXTO DO PROJETO

Este projeto implementa um simulador funcional para o processador didático RISC de 32 bits, o **UFLA-RISC**. O objetivo é fornecer uma ferramenta para a execução, depuração e teste de programas em nível de arquitetura de processador, como parte de estudos acadêmicos.

<h3 id="colab">👥 Colaboradores</h3>
<p>Os integrantes do grupo responsáveis por este projeto são:</p>

<table>
  <tr>
    <td align="center">
      <a href="#"> <img src="https://avatars.githubusercontent.com/u/134017049?v=4" width="100px;" alt="Foto de Clarisse Lacerda Pimentel"/>
        <br />
        <sub><b>Clarisse Lacerda Pimentel</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Clofender">
        <img src="https://avatars.githubusercontent.com/u/73314533?v=4" width="100px;" alt="Foto de Daniel Silva Ferraz Neto"/>
        <br />
        <sub><b>Daniel Silva Ferraz Neto</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="#"> <img src="https://avatars.githubusercontent.com/u/10137?v=4" width="100px;" alt="Foto de Helder Jose Avila"/>
        <br />
        <sub><b>Helder Jose Avila</b></sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/zector1">
        <img src="https://avatars.githubusercontent.com/u/137319815?v=4" width="100px;" alt="Foto de José Victor Miranda de Oliveira"/>
        <br />
        <sub><b>José Victor Miranda de Oliveira</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/MarcoTFranco">
        <img src="https://avatars.githubusercontent.com/u/121970508?v=4" width="100px;" alt="Foto de Marco Tulio Franco Silva"/>
        <br />
        <sub><b>Marco Tulio Franco Silva</b></sub>
      </a>
    </td>
  </tr>
</table>

## 2. INSTRUÇÕES PARA USO

### 🚀 Como Rodar o Assembler e o Simulador

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/MarcoTFranco/ufla-risc-simulador-grupo6-gcc123.git](https://github.com/MarcoTFranco/ufla-risc-simulador-grupo6-gcc123.git)
    ```

2.  **Monte seu código (Assembly → Binário):**
    Utilize o script principal do interpretador para converter seu `.asm` em `.bin`.
    ```bash
    # Sintaxe: python src/interpretador/main.py <entrada.asm> <saida.bin>
    python src/interpretador/main.py exemplos/01_teste_add.asm binarios/01_teste.bin
    ```

3.  **Execute o Simulador:**
    Com o binário gerado, execute o processador:
    ```bash
    # Exemplo de execução
    python src/simulador/main.py binarios/01_teste.bin
    ```

## 3. INSTRUÇÕES PARA DEVS

### 3.1. Pré-requisitos

-   **Python 3.x**

### 🧪 Rodando os Testes

Para verificar a integridade do sistema, você pode executar a bateria de testes unitários a partir da raiz do projeto:

```bash
python -m unittest discover
```
## 4. 🛠️ TECNOLOGIAS UTILIZADAS

- **Linguagem Principal:**
  - **Python 3: Utilizado para toda a lógica do simulador, parser e encoder.**
- **Testes:**
  - **Unittest: Biblioteca padrão do Python para validação das instruções.**

## 5. 📁 ESTRUTURA DO PROJETO

```
├── binarios/             # Arquivos binários (.bin) gerados e de teste
│
├── docs/                 # Documentação do projeto
│
├── exemplos/             # Exemplos de código Assembly (.asm)
│
├── src/
│   ├── interpretador/    # Módulo Assembler
│   │   ├── assembler.py  # Lógica de montagem
│   │   ├── encoder.py    # Codificação de instruções (32 bits)
│   │   ├── main.py       # CLI do Assembler
│   │   ├── opcodes.py    # Definição de Opcodes
│   │   └── parser.py     # Leitura e processamento de texto
│   │
│   └── simulador/        # Módulo do Processador
│       ├── simulador.py  # Núcleo de execução da CPU
│       └── main.py       # CLI do Simulador
│
├── .gitignore
└── README.md
```
## 5. 📁 LICENÇA

Projeto estritamente acadêmico, sem licença para uso comercial.
