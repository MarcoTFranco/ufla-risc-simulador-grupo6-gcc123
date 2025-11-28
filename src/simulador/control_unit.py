"""
control_unit.py - Unidade de Controle da CPU - VERSÃO MELHORADA

Implementa instruções de controle de fluxo (desvios e saltos)

"""


class ControlUnit:
    def __init__(self, cpu):
        self.cpu = cpu  # Recebe instância CPUState para atualizar PC/r31

    def beq(self, val_a, val_b, target_addr):
        """
        Branch if Equal.
        Se val_a == val_b, salta para target_addr.

        Args:
            val_a: Valor do registrador RA
            val_b: Valor do registrador RB
            target_addr: Endereço de destino (8 bits: 0-255)

        Returns:
            True se o branch foi tomado, False caso contrário

        """
        # Validar endereço de branch (0-255)
        target_addr = target_addr & 0xFF

        if val_a == val_b:
            self.cpu.set_pc(target_addr)
            return True
        return False

    def bne(self, val_a, val_b, target_addr):
        """
        Branch if Not Equal.
        Se val_a != val_b, salta para target_addr.

        Args:
            val_a: Valor do registrador RA
            val_b: Valor do registrador RB
            target_addr: Endereço de destino (8 bits: 0-255)

        Returns:
            True se o branch foi tomado, False caso contrário

        """
        # Validar endereço de branch (0-255)
        target_addr = target_addr & 0xFF

        if val_a != val_b:
            self.cpu.set_pc(target_addr)
            return True
        return False

    def jal(self, target_addr):
        """
        Jump and Link.
        Salva endereço de retorno (PC atual) em R31 e salta para target_addr.

        Args:
            target_addr: Endereço de destino (24 bits: 0-16777215)

        Exemplo:
            Endereço 10: JAL 100
            Após IF: PC = 11
            Após EX/MEM: R31 = 11, PC = 100
            Retorno: JR R31 → PC = 11 (próxima instrução após JAL)
        """
        # Validar endereço de jump (24 bits: 0-16777215)
        target_addr = target_addr & 0xFFFFFF

        # Salvar endereço de retorno (PC atual = PC+1 da instrução JAL)
        self.cpu.write_register(31, self.cpu.get_pc())

        # Saltar para endereço de destino
        self.cpu.set_pc(target_addr)

    def jr(self, reg_value):
        """
        Jump Register.
        Salta para o endereço contido em reg_value.

        Args:
            reg_value: Conteúdo do registrador RC (32 bits)

        Exemplo:
            JR R31  → PC = R31 (retorno de procedimento)
        """
        # Extrair apenas os bits válidos de endereço (16 bits)
        target_addr = reg_value & 0xFFFF
        self.cpu.set_pc(target_addr)

    def j(self, target_addr):
        """
        Jump Incondicional.
        Salta incondicionalmente para target_addr.

        Args:
            target_addr: Endereço de destino (24 bits: 0-16777215)

        Exemplo:
            J 500  → PC = 500
        """
        # Validar endereço de jump (24 bits: 0-16777215)
        target_addr = target_addr & 0xFFFFFF
        self.cpu.set_pc(target_addr)

    def get_branch_taken(self):
        """
        Retorna True se o último branch foi tomado.
        Útil para estatísticas de branch prediction.
        """
        pass
