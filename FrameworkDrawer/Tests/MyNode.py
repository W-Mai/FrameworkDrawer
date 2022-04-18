from FrameworkDrawer.FrameworkNode import ModelBoxBaseModel, Reg, Wire, CONFIGURE


class TestModel(ModelBoxBaseModel):
    CLK1 = Wire("CLK")
    RST = Wire("RST")
    D = Wire("D", (0, 31))
    Q = Reg("666", (0, 31))

    class Meta:
        name = "TestMode1l"


class TestModel2(ModelBoxBaseModel):
    CLK1 = Wire("CLK")
    RST = Wire("RST")
    D = Wire("D", (0, 31))
    Q2 = Reg("666", (0, 31))

    class Meta:
        name = "TestMode2"


CONFIG = CONFIGURE(
    node_pos_pair={
        TestModel: (0, 10),
        TestModel2: (10, 20),
    }, other_conf={
        TestModel: {
            "flag": True,
        }
    }, colors=[
        "#ffa502", "#ff6348", "#ff4757", "#747d8c",
        "#2f3542", "#2ed573", "#1e90ff", "#3742fa",
        "#e84393", "#05c46b", "#ffd43b", "#ffa000"
    ]
)
