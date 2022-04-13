# -*- coding: utf-8 -*-
#############################################
# File Name: setup.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-11
#############################################
from setuptools import setup, find_packages

setup(
    name="FrameworkDrawer",
    version="0.0.1",
    description="Draw a simple RTL block diagram.",
    long_description="A module for drawing simple RTL gate-level circuits.",
    author="W-Mai",
    author_email="1341398182@qq.com",
    url="https://github.com/W-Mai/FrameworkDrawer",
    license="MIT Licence",
    packages=find_packages(),
    install_requires=['schemdraw[svgmath]', 'pillow', 'xunionfind'],
)
