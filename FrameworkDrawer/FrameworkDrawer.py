#############################################
# File Name: FrameworkDrawer.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-11
#############################################
import inspect
import io
import json
from typing import IO, Union, Literal

import schemdraw
import schemdraw.elements as elm
from schemdraw import Segment, SegmentCircle, SegmentText, ImageFormat
from schemdraw.util import Point
from itertools import combinations, chain, tee
from xunionfind import UnionFind

from FrameworkDrawer.FrameworkNode import CONFIGURE, ModelBoxBaseModel
from FrameworkDrawer.FrameworkNode import Point as FPoint
from FrameworkDrawer.Signals import SignalBase


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class ConnectorBox(elm.Element):
    def __init__(self, source: str, target: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.source = source
        self.target = target
        self.label = f"{source}->{target}"

        self.anchors['center'] = (0, 0)


class ModelBox(elm.Element):
    def __init__(self, name, signals=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if signals is None:
            signals = []

        self.model_name = SegmentText((0, 0.5), name, fontsize=21)
        self.segments.append(self.model_name)

        real_width = (self.model_name.get_bbox().xmin + self.model_name.get_bbox().xmax) / 2

        for signal in signals:
            tmp_descriptor = signal['descriptor']
            descriptor = "" if tmp_descriptor[0] == 0 and tmp_descriptor[
                1] == 0 else f" [{tmp_descriptor[1]}, {tmp_descriptor[0]}]"

            sig_text = SegmentText((0, -0.6 * (signals.index(signal)) - 0.3), f"{signal['alias']}{descriptor}",
                                   fontsize=12)
            self.segments.append(sig_text)

            delta_width = (sig_text.get_bbox().xmin + sig_text.get_bbox().xmax) / 2
            if delta_width > real_width:
                real_width = delta_width

        padding_width = real_width + 0.5

        self.segments.append(Segment([(-padding_width, 1), (padding_width, 1)]))
        self.segments.append(Segment([(-padding_width, 0), (padding_width, 0)]))

        delta_y = 0
        for index in range(0, len(signals)):
            signal = signals[index]
            delta_y = -0.6 * (signals.index(signal)) - 0.6

            self.segments.append(SegmentCircle((-padding_width, delta_y + 0.3), 0.06, fill=True))
            self.segments.append(SegmentCircle((padding_width, delta_y + 0.3), 0.06, fill=True))
            self.anchors[signal['label'] + ".left"] = (-padding_width, delta_y + 0.3)
            self.anchors[signal['label'] + ".right"] = (padding_width, delta_y + 0.3)

            if index < len(signals) - 1:
                self.segments.append(Segment([(-padding_width, delta_y), (padding_width, delta_y)], lw=1))

        self.segments.append(Segment([(-padding_width, 1), (-padding_width, delta_y)]))
        self.segments.append(Segment([(padding_width, 1), (padding_width, delta_y)]))
        self.segments.append(Segment([(-padding_width, delta_y), (padding_width, delta_y)]))


class FrameworkDrawer(object):
    def __init__(self, file, is_model=False):
        self.file = file
        self.output_file = None
        if not is_model:
            if file is None:
                raise ValueError("json_file is Not Found")
            if isinstance(file, str):
                self.json_data = json.loads(file)
            else:
                self.json_data = json.load(file)
        else:
            if file is None:
                raise ValueError("Model is Not Found")
            buffer = io.StringIO()
            self.export_model_to_json(buffer)
            self.json_data = json.loads(buffer.getvalue())

    def draw(self, output_file, fmt: Union[
        Literal['eps', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'tif'], ImageFormat] = "svg"):
        if output_file is None:
            raise ValueError("output_file is None")

        with schemdraw.Drawing(show=False) as d:
            model_json = self.json_data

            COLORS = model_json['colors']
            connectors = model_json['connectors']
            connector_instance = dict()

            for connector in connectors:
                tmp_connectors = []
                for connector_pos in connector['positions']:
                    tmp_connectors.append(
                        d.add(ConnectorBox(connector['from'], connector['to']).at(connector_pos.values())))
                if len(tmp_connectors) == 0:
                    continue
                connector_instance[tmp_connectors[0].label] = tmp_connectors

            model_info = []
            model_instances = dict()

            for model in model_json['models']:
                pos = Point(model_json['drawing_info'][model['name']]['position'].values())
                flag = model_json['drawing_info'][model['name']].get('flag', False)
                model_instances[model['name']] = d.add(ModelBox(model['name'], model['signals']).at(pos))

                model_info.append({
                    'name': model['name'],
                    'pos': pos,
                    'flag': flag,
                    'signals': [s['label'] for s in model['signals']],
                })

            all_signals = {s for info in model_info for s in info['signals']}
            all_signals = chain(all_signals, [c for c in connector_instance])
            signal_color_map = {s: COLORS[i % len(COLORS)] for i, s in enumerate(sorted(all_signals))}
            # 1,2,3,4 combinations is
            # [1, 2] [1, 3] [1, 4] [2, 3] [2, 4] [3, 4]
            # [1, 2] [2, 3] [3, 4] [1, 3] [2, 4] [1, 4]
            model_info.sort(key=lambda x: x['pos'].x)
            model_combination = combinations(model_info, 2)
            model_combination = list(model_combination)

            model_wire_signal_model_set = dict()
            next_model_name = model_info[0]['name']
            while len(model_combination) > 0:
                try:
                    model_pair = next(filter(lambda m: m[0]['name'] == next_model_name, model_combination))
                except StopIteration:
                    model_pair = model_combination[0]
                next_model_name = model_pair[1]['name']
                model_combination.remove(model_pair)

                model_pair = list(model_pair)
                model_pair.sort(key=lambda x: x['pos'].x)

                left_model = model_pair[0]
                right_model = model_pair[1]

                def get_signal(model_name, signal_name, direction):
                    if direction == "left":
                        return getattr(model_instances[model_name], f"{signal_name}.left")
                    else:
                        return getattr(model_instances[model_name], f"{signal_name}.right")

                for signal in set(left_model['signals']).intersection(right_model['signals']):
                    if signal not in model_wire_signal_model_set:
                        model_wire_signal_model_set[signal] = UnionFind()
                    if model_wire_signal_model_set[signal].connected(left_model['name'], right_model['name']):
                        continue

                    left_signal_index = left_model['signals'].index(signal)
                    right_signal_index = right_model['signals'].index(signal)

                    model_wire_signal_model_set[signal].union(left_model['name'], right_model['name'])
                    left_model_left_signal = get_signal(left_model['name'], signal, 'left')
                    left_model_right_signal = get_signal(left_model['name'], signal, 'right')
                    right_model_left_signal = get_signal(right_model['name'], signal, 'left')
                    right_model_right_signal = get_signal(right_model['name'], signal, 'right')

                    if left_model_right_signal.x + 0.5 > right_model_left_signal.x:
                        # 当左模块的右边信号跟右模块的左边信号重合时
                        if right_model['flag']:
                            wire = elm.Wire(shape="c",
                                            k=right_model_right_signal.x - left_model_right_signal.x + 0.5 + left_signal_index / 4)
                            d.add(wire
                                  .at(left_model_right_signal)
                                  .to(right_model_right_signal)
                                  .color(signal_color_map[signal]))
                        else:
                            wire = elm.Wire(shape="c",
                                            k=-(0.5 + left_signal_index / 4))
                            d.add(wire
                                  .at(left_model_left_signal)
                                  .to(right_model_left_signal)
                                  .color(signal_color_map[signal]))
                    else:
                        # 当左模块的右边信号跟右模块的左边信号不重合时
                        k_left = 0.5 + left_signal_index / 4
                        k_right = 0.5 + right_signal_index / 4

                        if left_model_right_signal.y < right_model_left_signal.y:
                            if k_left < right_model_left_signal.x - left_model_right_signal.x:
                                d.add(elm.Wire("c", k=k_left).at(left_model_right_signal).to(
                                    right_model_left_signal)).color(signal_color_map[signal])
                            else:
                                d.add(elm.Wire("c", k=k_right).at(left_model_right_signal).to(
                                    right_model_left_signal)).color(signal_color_map[signal])

                        else:
                            if k_left < right_model_left_signal.x - left_model_right_signal.x:
                                d.add(elm.Wire("c", k=-k_left).at(right_model_left_signal).to(
                                    left_model_right_signal)).color(signal_color_map[signal])
                            else:
                                d.add(elm.Wire("c", k=-k_right).at(right_model_left_signal).to(
                                    left_model_right_signal)).color(signal_color_map[signal])

        for label, connectors in connector_instance.items():
            for con1, con2 in pairwise(connectors):
                k0 = (con1.center.x - con2.center.x) / 2
                d.add(elm.Wire("c", k=k0).at(con2.center).to(con1.center).color(signal_color_map[label]))
                # print(con1, con2, con1.center, con2.center)

            # 解析模块和信号

            def get_model_info(model_name):
                for model_i in model_info:
                    if model_i["name"] == model_name:
                        return model_i
                return None

            label: str
            (
                start_model_name, start_model_signal_name), (
                end_model_name, end_model_signal_name
            ) = [label.split('.') for label in label.split('->')]

            start_model_info = get_model_info(start_model_name)
            end_model_info = get_model_info(end_model_name)

            if start_model_info is None or end_model_info is None:
                continue

            start_signal_left = get_signal(start_model_name, start_model_signal_name, 'left')
            start_signal_right = get_signal(start_model_name, start_model_signal_name, 'right')
            end_signal_left = get_signal(end_model_name, end_model_signal_name, 'left')
            end_signal_right = get_signal(end_model_name, end_model_signal_name, 'right')

            start_connector = connectors[0]
            end_connector = connectors[-1]

            start_signal_index = start_model_info["signals"].index(start_model_signal_name)
            end_signal_index = end_model_info["signals"].index(end_model_signal_name)

            k0 = 0.5 + start_signal_index / 4
            if start_signal_left.x < start_connector.center.x < start_signal_right.x:
                d.add(elm.Wire("c", k=k0).at(start_signal_right).to(start_connector.center).color(
                    signal_color_map[label]))
            else:
                if start_signal_left.x > start_connector.center.x:
                    d.add(elm.Wire("c", k=-k0).at(start_signal_left).to(start_connector.center).color(
                        signal_color_map[label]))
                else:
                    d.add(elm.Wire("c", k=k0).at(start_signal_right).to(start_connector.center).color(
                        signal_color_map[label]))

            k0 = 0.5 + end_signal_index / 4
            if end_signal_left.x < end_connector.center.x < end_signal_right.x:
                d.add(elm.Wire("c", k=k0).at(end_signal_left).to(end_connector.center).color(signal_color_map[label]))
            else:
                if end_signal_left.x > end_connector.center.x:
                    d.add(elm.Wire("c", k=-k0).at(end_signal_left).to(end_connector.center).color(
                        signal_color_map[label]))
                else:
                    d.add(elm.Wire("c", k=k0).at(end_signal_right).to(end_connector.center).color(
                        signal_color_map[label]))

        if isinstance(output_file, str):
            d.save(output_file)
        if isinstance(output_file, IO):
            output_file.write(d.get_imagedata(fmt=fmt))

    def export_model_to_json(self, output_file, indent=None):
        module = self.file
        configures = inspect.getmembers(module, lambda member: isinstance(member, CONFIGURE))
        if len(configures) == 0:
            raise Exception('CONFIGURE class not found.')
        configure: CONFIGURE = configures[0][1]

        framework_draw_file_dict = {
            'drawing_info': {},
            'models': [],
            'connectors': [connector.to_dict() for connector in configure.CONNECTOR_PAIR],
            'colors': configure.COLORS,
        }

        for name, model in inspect.getmembers(module, lambda member: inspect.isclass(member)
                                                                     and issubclass(member, ModelBoxBaseModel)
                                                                     and not member == ModelBoxBaseModel):
            model_ins = model
            framework_draw_file_dict['models'].append(model_ins.to_dict())
            framework_draw_file_dict['drawing_info'][model_ins.name()] = model_ins.other_conf()

        if isinstance(output_file, str):
            json.dump(framework_draw_file_dict, open(output_file, 'w', encoding="utf-8"), default=lambda o: o.export,
                      indent=indent)
        else:
            json.dump(framework_draw_file_dict, output_file, default=lambda o: o.export, indent=indent)
        # print(framework_draw_file_dict)
