import json

import schemdraw
import schemdraw.elements as elm
from schemdraw import Segment, SegmentCircle, SegmentText
from schemdraw.elements import Wire
from schemdraw.util import Point
from itertools import combinations
from UnionFind import UnionFind


class FluxCapacitor(elm.Element):
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        radius = 0.075
        fclen = 0.5
        self.segments.append(SegmentCircle((0, 0), radius))
        self.segments.append(Segment([(0, 0), (0, -fclen * 1.41)]))
        self.segments.append(Segment([(0, 0), (fclen, fclen)]))
        self.segments.append(Segment([(0, 0), (-fclen, fclen)]))
        self.segments.append(SegmentCircle((0, -fclen * 1.41), 0.2, fill=None))
        self.segments.append(SegmentCircle((fclen, fclen), 0.2, fill=None))
        self.segments.append(SegmentCircle((-fclen, fclen), 0.2, fill=None))
        self.anchors['p1'] = (-fclen, fclen)
        self.anchors['p2'] = (fclen, fclen)
        self.anchors['p3'] = (0, -fclen * 1.41)


class ModelBox(elm.Element):
    def __init__(self, name, signals=None, *d, **kwargs):
        super().__init__(*d, **kwargs)
        if signals is None:
            signals = []

        self.model_name = SegmentText((0, 0.5), name, fontsize=21)
        self.segments.append(self.model_name)

        real_width = (self.model_name.get_bbox().xmin + self.model_name.get_bbox().xmax) / 2

        for signal in signals:
            tmp_descriptor = signal['descriptor']
            descriptor = "" if tmp_descriptor[0] == 0 and tmp_descriptor[
                1] == 0 else f" [{tmp_descriptor[1]}, {tmp_descriptor[0]}]"

            sig_text = SegmentText((0, -0.6 * (signals.index(signal)) - 0.3), f"{signal['label']}{descriptor}",
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


with schemdraw.Drawing(show=False) as d:
    doc = open("model.json", "r")
    model_json = json.load(doc)
    doc.close()

    model_info = []
    model_instances = dict()
    for model in model_json['models']:
        pos = Point(model_json['drawing_info'][model['name']]['position'].values())
        model_instances[model['name']] = d.add(ModelBox(model['name'], model['signals']).at(pos))

        model_info.append({
            'name': model['name'],
            'pos': pos,
            'signals': [s['label'] for s in model['signals']],
        })

    model_combination = combinations(model_info, 2)

    model_wire_signal_model_set = dict()
    for model_pair in model_combination:
        model_pair = list(model_pair)
        model_pair.sort(key=lambda x: x['pos'].x)

        left_model = model_pair[0]
        right_model = model_pair[1]

        for signal in set(left_model['signals']).intersection(right_model['signals']):
            if signal not in model_wire_signal_model_set:
                model_wire_signal_model_set[signal] = UnionFind()
            if model_wire_signal_model_set[signal].connected(left_model['name'], right_model['name']):
                continue

            model_wire_signal_model_set[signal].union(left_model['name'], right_model['name'])
            left_signal = getattr(model_instances[left_model['name']], f"{signal}.right", signal)
            right_signal = getattr(model_instances[right_model['name']], f"{signal}.left", signal)
            d.add(elm.Wire('z').at(left_signal).to(right_signal))

    print({u[0]: u[1].father for u in model_wire_signal_model_set.items()})

d.save("./imgs/schema.svg")
