# Author: W-Mai
# Date: 2022-04-11
# Project: FrameworkGraph

from FrameworkDrawer import FrameworkDrawer

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--fmt", type=str, default="svg")
    args = parser.parse_args()

    args_model_file = args.input
    args_output_file = args.output
    args_fmt = args.fmt

    with open(args_model_file, 'r') as f:
        fd = FrameworkDrawer(f)
        fd.draw(args_output_file, args_fmt)
