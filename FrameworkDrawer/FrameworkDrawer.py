#############################################
# File Name: FrameworkDrawer.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-11
#############################################

import json
from typing import IO, Union, Literal

import schemdraw
import schemdraw.elements as elm
from schemdraw import Segment, SegmentCircle, SegmentText, ImageFormat
from schemdraw.util import Point
from itertools import combinations
from xunionfind import UnionFind


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
    def __init__(self, json_file):
        self.output_file = None
        if json_file is None:
            raise ValueError("json_file is None")
        if isinstance(json_file, str):
            self.json_data = json.loads(json_file)
        else:
            self.json_data = json.load(json_file)

    def draw(self, output_file, fmt: Union[
        Literal['eps', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'tif'], ImageFormat] = "svg"):
        if output_file is None:
            raise ValueError("output_file is None")

        with schemdraw.Drawing(show=False) as d:
            model_json = self.json_data

            COLORS = model_json['colors']
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

                    signal_index = left_model['signals'].index(signal)

                    model_wire_signal_model_set[signal].union(left_model['name'], right_model['name'])
                    left_model_left_signal = get_signal(left_model['name'], signal, 'left')
                    left_model_right_signal = get_signal(left_model['name'], signal, 'right')
                    right_model_left_signal = get_signal(right_model['name'], signal, 'left')
                    right_model_right_signal = get_signal(right_model['name'], signal, 'right')

                    if left_model_right_signal.x + 0.5 > right_model_left_signal.x:
                        if right_model['flag']:
                            wire = elm.Wire(shape="c",
                                            k=right_model_right_signal.x - left_model_right_signal.x + 0.5 + signal_index / 3)
                            d.add(wire
                                  .at(left_model_right_signal)
                                  .to(right_model_right_signal)
                                  .color(signal_color_map[signal]))
                        else:
                            wire = elm.Wire(shape="c",
                                            k=-(0.5 + signal_index / 3))
                            d.add(wire
                                  .at(left_model_left_signal)
                                  .to(right_model_left_signal)
                                  .color(signal_color_map[signal]))
                    else:
                        d.add(elm.Wire("c", k=0.5 + signal_index / 3).at(left_model_right_signal).to(
                            right_model_left_signal)).color(signal_color_map[signal])

        if isinstance(output_file, str):
            d.save(output_file)
        if isinstance(output_file, IO):
            output_file.write(d.get_imagedata(fmt=fmt))
