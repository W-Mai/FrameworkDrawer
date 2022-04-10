import json

import schemdraw
import schemdraw.elements as elm
from schemdraw import Segment, SegmentCircle, SegmentText
from schemdraw.elements import Wire
from schemdraw.util import Point
from itertools import combinations


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


# with schemdraw.Drawing(show=False) as d:
#     model = d.add(ModelBox(name="ModelTest11111", signals=[
#         {
#             "label": "CLK",
#             "direction": "input",
#             "type": "wire",
#             "descriptor": [0, 0],
#             "alias": "CLK"
#         },
#         {
#             "label": "RST",
#             "descriptor": [0, 0],
#             "alias": "RST"
#         },
#         {
#             "label": "D",
#             "descriptor": [0, 3],
#             "alias": "D"
#         },
#         {
#             "label": "E",
#             "descriptor": [0, 3],
#             "alias": "D"
#         }
#     ]))
#     model2 = d.add(ModelBox(name="Model6", signals=[
#         {
#             "label": "CLK",
#             "descriptor": [0, 0],
#             "alias": "CLK"
#         },
#         {
#             "label": "RST",
#             "descriptor": [0, 0],
#             "alias": "RST"
#         },
#         {
#             "label": "D",
#             "descriptor": [0, 3],
#             "alias": "D"
#         },
#         {
#             "label": "E",
#             "descriptor": [0, 3],
#             "alias": "D"
#         }
#     ]).at([10, -5]))
#     # d.add(elm.Wire().at(res.start).to(getattr(model, 'p3')))
#     d.add(elm.Wire('z').at(getattr(model, "CLK.right")).to(getattr(model2, "CLK.left")))
#     d.add(elm.Wire('z').at(getattr(model, "RST.right")).to(getattr(model2, "RST.left")))
#     d.add(elm.Wire('z').at(getattr(model, "D.right")).to(getattr(model2, "D.left")))
#     d.add(elm.Wire('z').at(getattr(model, "E.right")).to(getattr(model2, "E.left")))
#
#     model3 = d.add(ModelBox(name="Model77", signals=[
#         {
#             "label": "CLK",
#             "descriptor": [0, 0],
#             "alias": "CLK"
#         },
#         {
#             "label": "RST",
#             "descriptor": [0, 0],
#             "alias": "RST"
#         },
#         {
#             "label": "D",
#             "descriptor": [0, 3],
#             "alias": "D"
#         },
#         {
#             "label": "E",
#             "descriptor": [0, 3],
#             "alias": "D"
#         }
#     ]).at([10, 5]))
#     d.add(elm.Arc3().at(getattr(model, "CLK.right")).to(getattr(model3, "CLK.left")))
#     d.add(elm.Arc3(1, -30, 30).at(getattr(model2, "CLK.right")).to(getattr(model3, "CLK.right")))
#     d.add(elm.Arc3().at(getattr(model, "RST.right")).to(getattr(model3, "RST.left")))
#     d.add(elm.Arc3().at(getattr(model, "D.right")).to(getattr(model3, "D.left")))
#     d.add(elm.Arc3().at(getattr(model, "E.right")).to(getattr(model3, "E.left")))

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
            'signals': [s['label'] for s in model['signals']]
        })

    model_combination = combinations(model_info, 2)
    for model_pair in model_combination:
        model_pair = list(model_pair)
        model_pair.sort(key=lambda x: x['pos'].x)

        left_model = model_pair[0]
        right_model = model_pair[1]

        for signal in set(left_model['signals']).intersection(right_model['signals']):
            left_signal = getattr(model_instances[left_model['name']], f"{signal}.right", signal)
            right_signal = getattr(model_instances[right_model['name']], f"{signal}.left", signal)
            d.add(elm.Wire('z').at(left_signal).to(right_signal))

        # model_info[model['name']]['signals'] = model['signals']

    print(model_info)

    # d.add(elm.Wire('z').at(getattr(model, "CLK.right")).to(getattr(model2, "CLK.left")))
    # d.add(elm.Wire('z').at(getattr(model, "RST.right")).to(getattr(model2, "RST.left")))
    # d.add(elm.Wire('z').at(getattr(model, "D.right")).to(getattr(model2, "D.left")))
    # d.add(elm.Wire('z').at(getattr(model, "E.right")).to(getattr(model2, "E.left")))
    #
    # d.add(elm.Arc3().at(getattr(model, "CLK.right")).to(getattr(model3, "CLK.left")))
    # d.add(elm.Arc3(1, -30, 30).at(getattr(model2, "CLK.right")).to(getattr(model3, "CLK.right")))
    # d.add(elm.Arc3().at(getattr(model, "RST.right")).to(getattr(model3, "RST.left")))
    # d.add(elm.Arc3().at(getattr(model, "D.right")).to(getattr(model3, "D.left")))
    # d.add(elm.Arc3().at(getattr(model, "E.right")).to(getattr(model3, "E.left")))

d.save("./imgs/schema.svg")

exit(0)

with schemdraw.Drawing() as d:
    d += elm.Resistor().right().label('1Ω')

with schemdraw.Drawing() as d:
    d += elm.Resistor().right().label('1Ω')
    d += elm.Capacitor().down().label('10μF')
    d += elm.Line().left()
    d += elm.SourceSin().up().label('10V')
