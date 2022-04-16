#############################################
# File Name: FrameworkNode.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-16
#############################################
import sys

from Signals import *


class ModelBoxBaseModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        mcs.attrs = attrs
        return type.__new__(mcs, name, bases, attrs)


class ModelBoxBaseModel(object, metaclass=ModelBoxBaseModelMetaclass):
    def __init__(self):
        for attr in ModelBoxBaseModel.attrs.items():
            sig_name: str = attr[0]
            sig_obj = attr[1]
            if isinstance(sig_obj, SignalBase):
                # sig_obj: SignalBase
                if sig_obj.alias is None:
                    setattr(sig_obj, 'alias', sig_name)

                print(sig_name, sig_obj.alias, sig_obj.label)


if __name__ == '__main__':
    class TestModel(ModelBoxBaseModel):
        CLK1 = Wire("CLK")
        RST = Wire("RST")
        D = Wire("D", (0, 31))
        Q = Reg("Q", (0, 31))

        class Meta:
            label = "TestModel"

    a = (__import__('FrameworkNode'))
    import inspect

    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            print(name, obj)

    print(a)

    m = TestModel()
