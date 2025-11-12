<h1 align="center" style="font-weight: bold;">
  Simulador Funcional do Processador UFLA-RISC
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
</p>

## 1. CONTEXTO DO PROJETO

Este projeto implementa um simulador funcional para o processador didático RISC de 32 bits, o **UFLA-RISC**. O objetivo é fornecer uma ferramenta para a execução, depuração e teste de programas em nível de arquitetura de processador, como parte de estudos acadêmicos.

<h3 id="colab">👥 Colaboradores</h3>
<p>Os integrantes do grupo responsáveis por este projeto são:</p>

<table>
  <tr>
    <td align="center">
      <a href="#"> <img src="https://avatars.githubusercontent.com/u/10137?v=4" width="100px;" alt="Foto de Clarisse Lacerda Pimentel"/>
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

### 🚀 Como Rodar o Simulador

1.  Clone o repositório:
    ```bash
    git clone https://github.com/MarcoTFranco/ufla-risc-simulador-grupo6-gcc123.git
    ```
2.  Navegue até a pasta do simulador:
    ```bash
    cd ufla-risc-simulador-grupo6-gcc123/src/simulador
    ```
3.  Execute o simulador principal:
    ```bash
    python main.py
    ```
4.  Para executar com um arquivo binário específico:
    ```bash
    python main.py binarios/programa.bin
    ```

## 3. INSTRUÇÕES PARA DEVS

### 3.1. Pré-requisitos

-   **Python 3.x**

### 3.2. Rodando os Testes

Para verificar a integridade do simulador e garantir que todas as funcionalidades estão corretas, execute a suíte de testes automatizados com `unittest`:

```bash
# Execute a partir da pasta raiz do projeto
python -m unittest discover
```
## 4. 🛠️ TECNOLOGIAS UTILIZADAS

- **Linguagem Principal:**
  - **Python 3: Utilizado para toda a lógica do simulador.**
- **Testes:**
  - **Unittest: Biblioteca padrão do Python para testes unitários.**

## 5. 📁 ESTRUTURA DO PROJETO

```
/ufla-risc-simulador-grupo6-gcc123/
├── binarios/
│   └── programa.bin  # Exemplo de binário para execução
│
├── src/
│   ├── simulador/
│   │   └── main.py     # Ponto de entrada do simulador
│   └── ...           # Outros módulos e testes
│
├── .gitignore
└── README.md         # Documentação do projeto
```
## 5. 📁 LICENÇA

Projeto estritamente acadêmico, sem licença para uso comercial.
