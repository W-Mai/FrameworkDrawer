#############################################
# File Name: Signals.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-16
#############################################

# {
#   "label":      "CLK",
#   "descriptor": [0, 0],
#   "alias":      "CLK"
# }
from typing import Tuple, Union


class Descriptor(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


class SignalBase(object):
    TYPE = None

    def __init__(self, label: str, descriptor: Union[Descriptor, Tuple] = Descriptor(0, 0), alias: str = None):
        self.label = label
        self.descriptor = Descriptor(*descriptor) if not isinstance(descriptor, Descriptor) else descriptor
        self.alias = alias


class Wire(SignalBase):
    TYPE = "Wire"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Reg(SignalBase):
    TYPE = "Reg"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
