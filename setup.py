# -*- coding: utf-8 -*-
#############################################
# File Name: setup.py
# Author: W-Mai
# Mail: 1341398182@qq.com
# Created Time:  2022-04-11
#############################################
from setuptools import setup, find_packages

long_description = """# FrameworkDrawer
一个绘制简单RTL门级电路的模块

使用方法如下：
```bash
python main.py [-h] --input INPUT --output OUTPUT [--fmt FMT]
```

用例：
```bash
 python .\main.py --input .\model.json --output .\imgs\schema.svg
```

输出的图片效果如下
<div style="background-color: white;">
<img src="https://github.com/W-Mai/FrameworkDrawer/blob/master/imgs/schema.svg">
</div>
"""


setup(
    name="FrameworkDrawer",
    version="0.0.4",
    description="Draw a simple RTL block diagram.",
    long_description=long_description,
    author="W-Mai",
    author_email="1341398182@qq.com",
    url="https://github.com/W-Mai/FrameworkDrawer",
    license="MIT Licence",
    packages=find_packages(),
    install_requires=['schemdraw[svgmath]', 'pillow', 'xunionfind'],
)
