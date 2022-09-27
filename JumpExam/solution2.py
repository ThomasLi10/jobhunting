# -*- coding: utf-8 -*-
#! /3rd/anaconda3/bin/ipython
"""
Author       : lixiang @ firebolt
Created Time : 2022-09-22 19:42:11
Description  : <Why this script>
"""

import ipdb

import math

def solution(S):
    files = get_binary_files(S)
    if files:
        min_len = math.inf
        for f in files:
            min_len = min(min_len,len(f))
        return str(min_len)
    else:
        return "NO FILES"

def get_binary_files(S):
    lines = S.split('\n')
    files = [l[11:] for l in lines if l[:6].replace(' ','')=='root' and l[7:10] in ['r--','r-x']]
    return [f for f in files if f.split('.')[-1] in ['doc','xls','pdf']]


S = '  root r-x delete-this.xls\n  root r-- bug-report.pdf\n  root r-- doc.xls\n  root r-- podcast.flac\n alice r-- system.xls\n  root --x invoices.pdf\n admin rwx SETUP.PY'

print(solution(S))
