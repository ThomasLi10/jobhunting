# -*- coding: utf-8 -*-
"""
# Author: lixiang
# Created Time : Fri 18 Mar 2022 07:58:55 PM CST
# File Name: test.py
# Description:
"""

json_string = '''
{
    "functions": {
        "f1": "log(sqrt + 10)",
        "f2": "f0**2 - f1 + 0.5*f1**2",
        "f0": "sum(pi)"
    },
    "values": {
        "y": [
            "mean(x) + log",
            "x**2"
        ],
        "x": "(f1 + f2) / (2 * pi)",
        "z": "f0*x / sum(x) * mean"
    }
}
'''

from ax import parse
import numpy as np



input = np.random.rand(10)
result = parse(json_string, input)
print(result)
