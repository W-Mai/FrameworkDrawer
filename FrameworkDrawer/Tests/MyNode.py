from FrameworkDrawer.FrameworkNode import ModelBoxBaseModel, Reg, Wire, CONFIGURE


class ALU(ModelBoxBaseModel):
    CLK = Wire('CLK')
    RST = Wire('RST')
    D = Wire('D')
    Q = Wire('Q')
    QN = Wire('QN')


class Core_Ctrl(ModelBoxBaseModel):
    CLK = Wire('CLK')
    Jump_Flag_In = Wire('Jump_Flag_In')
    Jump_Addr_In = Wire('Jump_Addr_In', (0, 31))

    Hold_Flag_EX_In = Wire('Hold_Flag_EX_In')
    Hold_Flag_RIB_In = Wire('Hold_Flag_RIB_In')
    Hold_Flag_CLINT_In = Wire('Hold_Flag_CLINT_In')

    Jtag_Halt_Flag_In = Wire('Jtag_Halt_Flag_In')

    Hold_Flag_Out = Wire('Hold_Flag_Out', (0, 2))
    Jump_Flag_Out = Wire('Jump_Flag_Out')
    Jump_Addr_Out = Wire('Jump_Addr_Out', (0, 31))

    class Meta:
        name = 'Core/Ctrl'


class Core_PC_REG(ModelBoxBaseModel):
    CLK = Wire('CLK')
    RST = Wire('RST')

    Jump_Flag_In = Wire('Jump_Flag_In')
    Jump_Addr_In = Wire('Jump_Addr_In', (0, 31))
    Hold_Flag_In = Wire('Hold_Flag_In', (0, 2))
    Jtag_Reset_Flag_In = Wire('Jtag_Reset_Flag_In')

    PC_Out = Wire('PC_Out', (0, 31))

    class Meta:
        name = 'Core/PC_REG'


class Core_REGS(ModelBoxBaseModel):
    CLK = Wire('CLK')
    RST = Wire('RST')

    Write_En_In = Wire('Write_En_In')
    Write_Addr_In = Wire('Write_Addr_In', (0, 4))
    Write_Data_In = Wire('Write_Data_In', (0, 31))

    Read_Addr1_In = Wire('Read_Addr1_In', (0, 4))
    Read_Addr2_In = Wire('Read_Addr2_In', (0, 4))

    Read_Data1_Out = Wire('Read_Data1_Out', (0, 31))
    Read_Data2_Out = Wire('Read_Data2_Out', (0, 31))

    class Meta:
        name = 'Core/REGS'


class Core_CSR_REG(ModelBoxBaseModel):
    CLK = Wire('CLK')
    RST = Wire('RST')

    Write_En_In = Wire('Write_En_In')
    Write_Addr_In = Wire('Write_Addr_In', (0, 31))
    Write_Data_In = Wire('Write_Data_In', (0, 31))

    Read_Addr_In = Wire('Read_Addr_In', (0, 31))

    Data_Out = Wire('Data_Out', (0, 31))

    CLINT_Write_En_In = Wire('CLINT_Write_En_In')
    CLINT_Write_Addr_In = Wire('CLINT_Write_Addr_In', (0, 31))
    CLINT_Write_Data_In = Wire('CLINT_Write_Data_In', (0, 31))
    CLINT_Read_Addr_In = Wire('CLINT_Read_Addr_In', (0, 31))
    CLINT_Data_Out = Wire('CLINT_Data_Out', (0, 31))
    CLINT_CSR_MTVEC = Reg('CLINT_CSR_MTVEC', (0, 31))
    CLINT_CSR_MEPC = Reg('CLINT_CSR_MEPC', (0, 31))
    CLINT_CSR_MSSTATUS = Reg('CLINT_CSR_MSSTATUS', (0, 31))

    class Meta:
        name = 'Core/CSR_REG'


class Core_IF_ID(ModelBoxBaseModel):
    CLK = Wire('CLK')
    RST = Wire('RST')

    Instruction_In = Wire('Instruction_In', (0, 31))
    Instruction_Addr_In = Wire('Instruction_Addr_In', (0, 31))

    Hold_Flag_In = Wire('Hold_Flag_In')
    Int_Flag_In = Wire('Int_Flag_In')

    Int_Flag_Out = Wire('Int_Flag_Out')
    Instruction_Out = Wire('Instruction_Out', (0, 31))
    Instruction_Addr_Out = Wire('Instruction_Addr_Out', (0, 31))

    class Meta:
        name = 'Core/IF_ID'


class Core_ID(ModelBoxBaseModel):
    CLK = Wire('CLK')

    Instruction_In = Wire('Instruction_In', (0, 31))
    Instruction_Addr_In = Wire('Instruction_Addr_In', (0, 31))

    Reg1_Read_Data_In = Wire('Reg1_Read_Data_In', (0, 31))
    Reg2_Read_Data_In = Wire('Reg2_Read_Data_In', (0, 31))

    CSR_Read_Data_In = Wire('CSR_Read_Data_In', (0, 31))

    EX_Jump_Flag_In = Wire('EX_Jump_Flag_In')
    Reg1_Read_Addr_Out = Wire('Reg1_Read_Addr_Out', (0, 4))
    Reg2_Read_Addr_Out = Wire('Reg2_Read_Addr_Out', (0, 4))

    CSR_Read_Addr_Out = Wire('CSR_Read_Addr_Out', (0, 31))
    MEM_Req_Out = Wire('MEM_Req_Out')

    Instruction_Out = Wire('Instruction_Out', (0, 31))
    Instruction_Addr_Out = Wire('Instruction_Addr_Out', (0, 31))
    Reg1_Read_Data_Out = Wire('Reg1_Read_Data_Out', (0, 31))
    Reg2_Read_Data_Out = Wire('Reg2_Read_Data_Out', (0, 31))

    Reg_Write_En_Out = Wire('Reg_Write_En_Out')
    Reg_Write_Addr_Out = Wire('Reg_Write_Addr_Out', (0, 4))
    CSR_Write_En_Out = Wire('CSR_Write_En_Out')
    CSR_Read_Data_Out = Wire('CSR_Read_Data_Out', (0, 31))
    CSR_Write_Addr_Out = Wire('CSR_Write_Addr_Out', (0, 31))

    class Meta:
        name = 'Core/ID'


CONFIG = CONFIGURE(
    node_pos_pair={
        ALU: (-1, 15),
        Core_Ctrl: (-6.5, 5),
        Core_PC_REG: (-35, 0),
        Core_REGS: (-45, 15),
        Core_CSR_REG: (-55, 15),
        Core_IF_ID: (-26, 5),
        Core_ID: (-15, 2),
    }, other_conf={
        ALU: {
            'flag': True
        },
        Core_IF_ID: {
            'flag': True
        },
    }, colors=[
        "#ffa502", "#ff6348", "#ff4757", "#747d8c",
        "#2f3542", "#2ed573", "#1e90ff", "#3742fa",
        "#e84393", "#05c46b", "#ffd43b", "#ffa000"
    ]
)
