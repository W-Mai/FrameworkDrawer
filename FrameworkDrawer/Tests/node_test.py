#############################################
# File Name: FrameworkDrawer.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-13
#############################################
import time

from FrameworkDrawer import FrameworkDrawer

if __name__ == '__main__':
    t0 = time.time()
    fd = FrameworkDrawer(file=open("../../model.json"), is_model=False)
    fd.draw("../../imgs/schema.svg")
    print("Time:", time.time() - t0)

    # import MyNode
    #
    # fd = FrameworkDrawer(file=MyNode, is_model=True)
    # fd.export_model_to_json(open("../../model.json", "w"))
