#############################################
# File Name: FrameworkNode.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-16
#############################################
from optparse import Option
from typing import Dict, Type, Optional, List, Tuple
from .Signals import *


# {
#       "name":    "ModelName",
#       "signals": [],
# }
#

class Point(object):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(x={}, y={})".format(self.x, self.y)

    @property
    def export(self):
        return {
            "x": self.x,
            "y": self.y
        }


class ModelBoxBaseModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        mcs._attrs = None
        mcs._signals = None

        attrs["_attrs"] = attrs

        signals = []
        for attr in attrs.items():
            sig_name: str = attr[0]
            sig_obj = attr[1]
            if isinstance(sig_obj, SignalBase):
                # sig_obj: SignalBase
                if sig_obj.alias is None:
                    setattr(sig_obj, 'alias', sig_name)
                sig_obj.model = ""
                signals.append(sig_obj)
        attrs['_signals'] = signals

        obj = super().__new__(mcs, name, bases, attrs)
        for sig in obj._signals:
            sig.model = obj

        return obj


class ModelBoxBaseModel(object, metaclass=ModelBoxBaseModelMetaclass):
    class Meta:
        pass

    def __init__(self):
        pass

    @classmethod
    def to_dict(cls):
        meta_dict = cls.meta_dict()
        res_dict = {
            # 如果name为空，则使用类名
            'name': cls.name(),
            'signals': [sig.to_dict() for sig in cls.signals()]
        }

        return res_dict

    @classmethod
    def other_conf(cls):
        meta_dict = cls.meta_dict()
        res_dict = {
            conf_name:
                meta_dict.get(conf_name, None)
            for conf_name in cls.readable_conf() if meta_dict.get(conf_name, None) is not None
        }
        return res_dict

    # 哪些配置项可以读取
    @staticmethod
    def readable_conf():
        return ["position", "flag"]

    @classmethod
    def meta_dict(cls):
        meta_class = cls.Meta
        if meta_class is not None:
            return {
                conf_name: getattr(meta_class, conf_name, None)
                for conf_name in cls.readable_conf()
            }

    @classmethod
    def attrs(cls):
        return cls._attrs

    @classmethod
    def signals(cls):
        return cls._signals

    @property
    def name(self):
        return self.meta_dict.get('name', type(self).__name__)


class Connector(object):
    def __init__(self, start_signal: SignalBase, end_signal: SignalBase, *positions: Tuple[int, int]):
        self.start_signal = start_signal
        self.end_signal = end_signal

        self.positions = []
        for pos in positions:
            self.positions.append(Point(*pos))

    def __str__(self):
        return "Connector(start={}, end={}, positions={})".format(self.start_signal, self.end_signal, self.positions)

    def to_dict(self):
        return {
            "from": f"{self.start_signal}.{self.start_signal.label}",
            "to": self.end_signal.alias,
            "positions": [pos.export for pos in self.positions]
        }


class CONFIGURE(object):

    def __init__(self,
                 node_pos_pair: Dict[Type[ModelBoxBaseModel], Tuple[int, int]],
                 other_conf=None,
                 colors=None):
        if colors is None:
            colors = [
                "#ffa502", "#ff6348", "#ff4757", "#747d8c",
                "#2f3542", "#2ed573", "#1e90ff", "#3742fa",
                "#e84393", "#05c46b", "#ffd43b", "#ffa000"
            ]
        if other_conf is None:
            other_conf = dict()
        self.POSITIONS_PAIR = node_pos_pair
        self.COLORS = colors
        self.OTHER_CONF = other_conf

        for node, pos in node_pos_pair.items():
            node.Meta.position = Point(*pos)

        for node, conf in other_conf.items():
            for attr in conf.items():
                setattr(node.Meta, attr[0], attr[1])
