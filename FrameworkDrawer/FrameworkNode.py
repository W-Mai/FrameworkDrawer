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

class ModelBoxBaseModelMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        mcs._attrs = attrs.copy()
        attrs["_attrs"] = attrs
        return super().__new__(mcs, name, bases, attrs)

    @property
    def attrs(self):
        return self._attrs


class ModelBoxBaseModel(object, metaclass=ModelBoxBaseModelMetaclass):
    Meta = None

    def __init__(self):
        self._signals = []

        for attr in type(self).attrs.items():
            sig_name: str = attr[0]
            sig_obj = attr[1]
            if isinstance(sig_obj, SignalBase):
                # sig_obj: SignalBase
                if sig_obj.alias is None:
                    setattr(sig_obj, 'alias', sig_name)
                self._signals.append(sig_obj)

    def to_dict(self):
        meta_dict = self.meta_dict

        res_dict = {
            conf_name:
                meta_dict.get(conf_name, None)
            for conf_name in self.readable_conf() if meta_dict.get(conf_name, None) is not None
        }
        res_dict['signals'] = [sig.to_dict() for sig in self._signals]

        # 如果name为空，则使用类名
        if meta_dict.get('name', None) is not None:
            res_dict['name'] = type(self).__name__

        return res_dict

    # 哪些配置项可以读取
    @staticmethod
    def readable_conf():
        return ["name", "position", "flag"]

    @property
    def meta_dict(self):
        meta_class = type(self).Meta
        if meta_class is not None:
            return {
                conf_name: getattr(meta_class, conf_name, None)
                for conf_name in self.readable_conf()
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
            node.Meta.position = pos

        for node, conf in other_conf.items():
            for attr in conf.items():
                setattr(node.Meta, attr[0], attr[1])
