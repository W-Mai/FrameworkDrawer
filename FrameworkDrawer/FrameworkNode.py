#############################################
# File Name: FrameworkNode.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-16
#############################################
import sys

from Signals import *


# {
#       "name":    "ModelName",
#       "signals": [],
# }
#

class ModelBoxBaseModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        mcs._attrs = attrs
        return type.__new__(mcs, name, bases, attrs)

    @property
    def attrs(self):
        return self._attrs

    @property
    def meta_dict(self):
        meta_class = ModelBoxBaseModel.attrs.get('Meta', None)
        if meta_class is not None:
            return {
                'name': getattr(meta_class, 'name', None),
            }


class ModelBoxBaseModel(object, metaclass=ModelBoxBaseModelMetaclass):
    def __init__(self):
        self._signals = []

        for attr in ModelBoxBaseModel.attrs.items():
            sig_name: str = attr[0]
            sig_obj = attr[1]
            if isinstance(sig_obj, SignalBase):
                # sig_obj: SignalBase
                if sig_obj.alias is None:
                    setattr(sig_obj, 'alias', sig_name)
                self._signals.append(sig_obj)

    def to_dict(self):
        meta_class = ModelBoxBaseModel.meta_dict

        return {
            "name": meta_class.get('name', self.__class__.__name__),
            "signals": [sig.to_dict() for sig in self._signals]
        }


if __name__ == '__main__':

    class TestModel(ModelBoxBaseModel):
        CLK1 = Wire("CLK")
        RST = Wire("RST")
        D = Wire("D", (0, 31))
        Q = Reg("Q", (0, 31))

        class Meta:
            name = "TestMode1l"


    # a = (__import__('FrameworkNode'))
    import inspect

    for name, model in filter(
            lambda x: inspect.isclass(x[1]) and issubclass(x[1], ModelBoxBaseModel) and not x[1] == ModelBoxBaseModel,
            inspect.getmembers(sys.modules[__name__])):
        # print(name, model)
        print(model().to_dict())
