"""
simulator.py - Simulador com Pipeline de 4 Estágios

"""

from alu import ALU
from control_unit import ControlUnit
from cpu_state import CPUState
from instruction_decoder import InstructionDecoder
from memory import Memory


class Simulator:
    def __init__(self, verbose=False):
        """
        Inicializa simulador.

        Args:
            verbose: Se True, imprime cada ciclo. Se False, apenas resumo.
        """
        self.cpu = CPUState()
        self.memory = Memory()
        self.alu = ALU()
        self.decoder = InstructionDecoder()
        self.control = ControlUnit(self.cpu)
        self.halted = False
        self.cycle_counter = 0
        self.instruction_count = 0
        self.verbose = verbose

        # Controle de pipeline
        self.current_stage = 'IF'
        self.stage_counter = 0

        # Registradores de estágio
        self.decoded = None
        self.opcode = 0
        self.ra = self.rb = self.rc = 0
        self.const16 = self.address = 0
        self.branch_offset = 0
        self.val_a = self.val_b = self.val_c = 0
        self.write_enable = False
        self.alu_result = 0
        self.mem_data = 0
        self.is_halt_instruction = False

        # Snapshot para detectar mudanças
        self.previous_state = None

    def execute_cycle(self):
        """Executa UM ciclo de clock (um estágio)"""
        if self.halted:
            return False

        # Capturar estado antes do ciclo
        self.previous_state = self.cpu.snapshot()

        # Executar estágio apropriado
        if self.current_stage == 'IF':
            self.stage_if()
            if self.verbose:
                self.print_cycle_changes('IF')
            self.current_stage = 'ID'

        elif self.current_stage == 'ID':
            self.stage_id()
            if self.verbose:
                self.print_cycle_changes('ID')
            self.current_stage = 'EX_MEM'

        elif self.current_stage == 'EX_MEM':
            self.stage_ex_mem()
            if self.verbose:
                self.print_cycle_changes('EX_MEM')
            self.current_stage = 'WB'

        elif self.current_stage == 'WB':
            self.stage_wb()
            if self.verbose:
                self.print_cycle_changes('WB')
            self.current_stage = 'IF'
            self.instruction_count += 1

        self.cycle_counter += 1
        return True

    def print_cycle_changes(self, stage_name):
        """Imprime modificações ocorridas no ciclo (MODO VERBOSO)"""
        print(f"\n{'='*70}")
        print(f"CICLO {self.cycle_counter + 1} - Estágio: {stage_name}")
        print(f"Instrução #{self.instruction_count + 1}")
        print(f"{'='*70}")

        if stage_name == 'IF':
            print(f"IR <- 0x{self.cpu.get_ir():08x}")
            print(f"PC <- {self.cpu.get_pc()} (0x{self.cpu.get_pc():04x})")
            if self.decoded:
                print(
                    f"Instrução: {self.decoder.format_instruction(self.decoded)}")

        elif stage_name == 'ID':
            print("Decodificação da instrução")
            print(
                f"Opcode: 0x{self.opcode:02x} ({self.decoder.get_mnemonic(self.opcode)})")
            print(f"Operandos lidos:")
            if self.ra < 32:
                print(f"  RA (R{self.ra}) = 0x{self.val_a:08x}")
            if self.rb < 32 and self.decoder.get_instruction_type(self.opcode) in ['type_3reg', 'type_branch']:
                print(f"  RB (R{self.rb}) = 0x{self.val_b:08x}")
            print("(Sem alterações em registradores/memória)")

        elif stage_name == 'EX_MEM':
            print("Execução da instrução")
            if self.opcode == 0x11:
                addr = self.val_c & 0xFFFF
                print(f"Memória[{addr}] <- 0x{self.val_a:08x}")
            elif self.opcode == 0x10:
                addr = self.val_a & 0xFFFF
                print(f"Leitura: Memória[{addr}] = 0x{self.mem_data:08x}")
            elif self.write_enable:
                print(f"Resultado ALU: 0x{self.alu_result:08x}")

            if self.decoder.affects_flags(self.opcode):
                flags = self.cpu.get_flags_dict()
                print(
                    f"Flags (CPU): N={flags['neg']} Z={flags['zero']} C={flags['carry']} V={flags['overflow']}")

        elif stage_name == 'WB':
            if self.write_enable and self.rc != 0:
                if self.opcode == 0x10:
                    print(f"R{self.rc} <- 0x{self.mem_data:08x} (Write-Back)")
                else:
                    print(f"R{self.rc} <- 0x{self.alu_result:08x} (Write-Back)")
            else:
                print("(Sem write-back)")

    def stage_if(self):
        """IF: Busca instrução e incrementa PC"""
        if self.halted:
            return
        pc = self.cpu.get_pc()
        instruction = self.memory.read(pc)
        self.cpu.set_ir(instruction)
        self.cpu.increment_pc()

    def stage_id(self):
        """ID: Decodifica instrução e lê registradores"""
        self.decoded = self.decoder.decode(self.cpu.get_ir())
        self.opcode = self.decoded['opcode']
        self.ra = self.decoded['ra']
        self.rb = self.decoded['rb']
        self.rc = self.decoded['rc']
        self.const16 = self.decoded['const16']
        self.address = self.decoded['address']
        self.branch_offset = self.decoded['branch_offset']
        self.val_a = self.cpu.read_register(self.ra)
        self.val_b = self.cpu.read_register(self.rb)
        self.val_c = self.cpu.read_register(self.rc)

    def stage_ex_mem(self):
        """
        EX/MEM: Executa operação e acessa memória
        """
        self.write_enable = False
        self.alu_result = 0
        self.is_halt_instruction = False
        op = self.opcode

        # ALU Operations
        if op == 0x01:  # ADD
            self.alu_result = self.alu.add(self.val_a, self.val_b)
            self.write_enable = True

        elif op == 0x02:  # SUB
            self.alu_result = self.alu.sub(self.val_a, self.val_b)
            self.write_enable = True

        elif op == 0x03:  # ZEROS - CORRIGIDO: sem parâmetro
            self.alu_result = self.alu.zeros()
            self.write_enable = True

        elif op == 0x04:  # XOR
            self.alu_result = self.alu.xor(self.val_a, self.val_b)
            self.write_enable = True

        elif op == 0x05:  # OR
            self.alu_result = self.alu.or_op(self.val_a, self.val_b)
            self.write_enable = True

        elif op == 0x06:  # NOT
            self.alu_result = self.alu.not_op(self.val_a)
            self.write_enable = True

        elif op == 0x07:  # AND
            self.alu_result = self.alu.and_op(self.val_a, self.val_b)
            self.write_enable = True

        elif op in (0x08, 0x09, 0x0A, 0x0B):  # Shifts
            shift = self.val_b & 0x1F
            if op == 0x08:
                self.alu_result = self.alu.asl(self.val_a, shift)
            elif op == 0x09:
                self.alu_result = self.alu.asr(self.val_a, shift)
            elif op == 0x0A:
                self.alu_result = self.alu.lsl(self.val_a, shift)
            elif op == 0x0B:
                self.alu_result = self.alu.lsr(self.val_a, shift)
            self.write_enable = True

        elif op == 0x0C:  # PASSA
            self.alu_result = self.alu.copy(self.val_a)
            self.write_enable = True

        elif op == 0x0E:  # LCH
            self.alu_result = self.alu.load_const_high(
                self.val_c, self.const16)
            self.write_enable = True

        elif op == 0x0F:  # LCL
            self.alu_result = self.alu.load_const_low(self.val_c, self.const16)
            self.write_enable = True

        # Memory Operations
        elif op == 0x10:  # LOAD
            addr = self.val_a & 0xFFFF
            self.mem_data = self.memory.read(addr)
            self.write_enable = True

        elif op == 0x11:  # STORE
            addr = self.val_c & 0xFFFF
            self.memory.write(addr, self.val_a)

        # Control Flow
        elif op == 0x12:  # JAL
            self.control.jal(self.address)

        elif op == 0x13:  # JR
            self.control.jr(self.val_c)

        elif op == 0x14:  # BEQ - CORRIGIDO: validação de range
            target = self.branch_offset & 0xFF  # Garantir 8 bits (0-255)
            self.control.beq(self.val_a, self.val_b, target)

        elif op == 0x15:  # BNE - CORRIGIDO: validação de range
            target = self.branch_offset & 0xFF  # Garantir 8 bits (0-255)
            self.control.bne(self.val_a, self.val_b, target)

        elif op == 0x16:  # J
            self.control.j(self.address)

        # Additional Instructions
        elif op == 0x17:  # SLT
            self.alu_result = self.alu.slt(self.val_a, self.val_b)
            self.write_enable = True

        elif op == 0x18:  # MUL
            self.alu_result = self.alu.mul(self.val_a, self.val_b)
            self.write_enable = True

        elif op == 0x19:  # DIV
            self.alu_result = self.alu.div(self.val_a, self.val_b)
            self.write_enable = True

        elif op == 0x1A:  # MOD
            self.alu_result = self.alu.mod(self.val_a, self.val_b)
            self.write_enable = True

        elif op == 0x1B:  # NEG
            self.alu_result = self.alu.neg(self.val_a)
            self.write_enable = True

        elif op == 0x1C:  # INC
            self.alu_result = self.alu.inc(self.val_a)
            self.write_enable = True

        elif op == 0x1D:  # DEC
            self.alu_result = self.alu.dec(self.val_a)
            self.write_enable = True

        elif op == 0x1E:  # NOP
            pass

        elif op == 0xFF:  # HALT
            self.is_halt_instruction = True

        else:
            print(f"\n⚠️  ERRO: Opcode inválido 0x{op:02x} detectado!")
            print(f"Instrução: 0x{self.cpu.get_ir():08x}")
            print(f"PC: {self.cpu.get_pc() - 1}")
            print("Encerrando simulação...")
            self.halted = True

        # CORREÇÃO CRÍTICA: Atualizar flags da CPU em EX/MEM
        # (não em WB como estava antes)
        if self.decoder.affects_flags(self.opcode):
            alu_flags = self.alu.get_flags()
            self.cpu.set_flags(
                neg=alu_flags['neg'],
                zero=alu_flags['zero'],
                carry=alu_flags['carry'],
                overflow=alu_flags['overflow']
            )

    def stage_wb(self):
        """
        WB: Escreve resultado no registrador

        CORRIGIDO: Flags NÃO são mais atualizados aqui (já foram em EX/MEM)
        """
        if self.write_enable and self.rc != 0:
            if self.opcode == 0x10:
                self.cpu.write_register(self.rc, self.mem_data)
            else:
                self.cpu.write_register(self.rc, self.alu_result)

        # Garantir que R0 sempre seja 0
        self.cpu.write_register(0, 0)

        if self.is_halt_instruction:
            self.halted = True

    def run(self, max_cycles=100000):
        """Executa simulação completa"""
        self.halted = False
        self.cycle_counter = 0
        self.instruction_count = 0
        self.current_stage = 'IF'

        print("\n" + "="*70)
        print("INICIANDO SIMULAÇÃO UFLA-RISC")
        if self.verbose:
            print("MODO: VERBOSO (mostrando todos os ciclos)")
        else:
            print("MODO: SILENCIOSO (apenas resumo final)")
        print("="*70)

        while self.cycle_counter < max_cycles:
            if not self.execute_cycle():
                break

        print("\n" + "="*70)
        print("SIMULAÇÃO FINALIZADA")
        print("="*70)
        print(f"Total de ciclos: {self.cycle_counter}")
        print(f"Total de instruções: {self.instruction_count}")

        if self.instruction_count > 0:
            cpi = self.cycle_counter / self.instruction_count
            print(f"CPI (Cycles Per Instruction): {cpi:.2f}")
            if cpi == 4.0:
                print("✓ CPI perfeito! (4 estágios por instrução)")
            else:
                print(f"⚠️  CPI esperado: 4.0 | Real: {cpi:.2f}")
        else:
            print("CPI: N/A (nenhuma instrução executada)")
