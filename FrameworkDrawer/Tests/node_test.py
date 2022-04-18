import sys
import unittest
import inspect

from FrameworkDrawer.FrameworkNode import ModelBoxBaseModel, CONFIGURE

if __name__ == '__main__':

    a = (__import__('MyNode'))
    configures = inspect.getmembers(a, lambda member: isinstance(member, CONFIGURE))
    if len(configures) == 0:
        raise Exception('CONFIGURE class not found.')
    configure: CONFIGURE = configures[0][1]
    print(configure.COLORS)
    for name, model in filter(
            lambda x: inspect.isclass(x[1]) and issubclass(x[1], ModelBoxBaseModel) and not x[1] == ModelBoxBaseModel,
            inspect.getmembers(a)):
        # print(model().to_dict())
        print(model().to_dict())
