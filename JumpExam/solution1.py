# -*- coding: utf-8 -*-
#! /3rd/anaconda3/bin/ipython
"""
Author       : lixiang @ firebolt
Created Time : 2022-09-22 19:58:00
Description  : <Why this script>
"""

import ipdb

from statistics import median

def solution(A, B):
    idx = sorted(range(len(B)), key=lambda k: B[k])
    sA = [A[i] for i in idx]
    sB = [B[i] for i in idx]

    for i in range(1,len(A))[::-1]:
        J = joint(sA[i-1:i+1],sB[i-1:i+1])
        if len(J[0])==1:
            sA[i] = J[0][0]
            sB[i] = J[1][0]
            sA.pop(i-1)
            sB.pop(i-1)
    print(sA,sB)
        
    return len(sA)


def joint(A,B):
    if B[0] < A[1] or B[1] < A[0]:
        return A,B
    else:
        return [min(A)],[max(B)]


A = [1,12,42,70,36,-4,43,15]
B = [5,15,44,72,36, 2,69,24]

A1 = [1,12,42,70,36,-4,43,15,2]
B1 = [5,15,44,72,36, 2,69,24,23]

A2 = [1,12,42,70,36,-4,43,15,69]
B2 = [5,15,44,72,36, 2,69,24,80]

print(solution(A,B))
print(solution(A1,B1))
print(solution(A2,B2))
