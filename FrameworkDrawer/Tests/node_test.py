import json
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
    framework_draw_file_dict = {
        'drawing_info': {},
        'models': [],
        'colors': configure.COLORS,
    }

    for name, model in filter(
            lambda x: inspect.isclass(x[1]) and issubclass(x[1], ModelBoxBaseModel) and not x[1] == ModelBoxBaseModel,
            inspect.getmembers(a)):
        model_ins = model()
        framework_draw_file_dict['models'].append(model_ins.to_dict())
        framework_draw_file_dict['drawing_info'][name] = model_ins.other_conf

    print(json.dumps(framework_draw_file_dict, default=lambda o: o.export))
    json.dump(framework_draw_file_dict, open('../../model.json', 'w'), default=lambda o: o.export)
    # print(framework_draw_file_dict)
