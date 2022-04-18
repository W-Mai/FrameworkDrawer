from FrameworkDrawer.FrameworkNode import ModelBoxBaseModel, Reg, Wire, CONFIGURE


class TestModel(ModelBoxBaseModel):
    CLK1 = Wire("CLK")
    RST = Wire("RST")
    D = Wire("D", (0, 31))
    Q = Reg("Q", (0, 31))

    class Meta:
        name = "TestMode1l"


class TestModel2(ModelBoxBaseModel):
    CLK1 = Wire("CLK")
    RST = Wire("RST")
    D = Wire("D", (0, 31))
    Q2 = Reg("QQQ", (0, 31))

    class Meta:
        name = "TestMode2"


CONFIG = CONFIGURE(node_pos_pair={
    TestModel: (0, 10),
    TestModel2: (0, 20),
}, other_conf={
    TestModel: {
        "flag": True,
    }
})
