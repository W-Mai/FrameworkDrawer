# Author: W-Mai
# Date: 2022-04-11
# Project: FrameworkGraph

from FrameworkDrawer import FrameworkDrawer

import os
import time

last_time = 0


def is_any_file_changed(filename):
    global last_time
    try:
        mtime = os.stat(filename).st_mtime
    except IOError:
        return False

    if mtime > last_time:
        last_time = mtime
        return True
    return False


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--fmt", type=str, default="svg")
    parser.add_argument("--auto-reload", type=bool, default=False)
    args = parser.parse_args()

    args_model_file = args.input
    args_output_file = args.output
    args_fmt = args.fmt
    args_auto_reload = args.auto_reload

    if args_auto_reload:
        while True:
            if is_any_file_changed(args_model_file):
                print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Reloading...')
                with open(args_model_file, 'r') as f:
                    fd = FrameworkDrawer(f)
                    fd.draw(args_output_file, args_fmt)
                print(f'{time.strftime("%Y-%m-%d %H:%M:%S")} Reload success!')
            time.sleep(1)
    else:
        with open(args_model_file, 'r') as f:
            fd = FrameworkDrawer(f)
            fd.draw(args_output_file, args_fmt)


if __name__ == '__main__':
    main()
