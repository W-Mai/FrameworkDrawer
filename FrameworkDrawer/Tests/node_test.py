#############################################
# File Name: FrameworkDrawer.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-13
#############################################
import time

from FrameworkDrawer import FrameworkDrawer
from FrameworkDrawer.FrameworkNode import Connector

if __name__ == '__main__':
    t0 = time.time()
    fd = FrameworkDrawer(file=__import__("MyNode"), is_model=True)
    fd.draw("../../imgs/schema.svg")
    print("Time:", time.time() - t0)

    #
    # fd = FrameworkDrawer(file=MyNode, is_model=True)
    # fd.export_model_to_json(open("../../model.json", "w"))
