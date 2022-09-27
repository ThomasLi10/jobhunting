# -*- coding: utf-8 -*-
"""
# Author: lixiang@firebolt
# Created Time : Fri 12 Aug 2022 08:13:05 PM CST
# File Name: JingDongShopping.py
# Description:
"""

'''
JingDong's "618" shopping festival has various promotional activities, such as "200-50" (the total price will minus 50 if you meet 200 yuan). Suppose there are n products you want to buy in your girlfriend’s shopping list. She wants to choose a few of them. Under the premise of enough conditions, the total price of the selected products should be as close as possible. Full minus conditions (200 yuan), so that you can "scramble wool" to the utmost extent. As a programmer, can you write a code to help her get it?

Supposed array “items” is the price of each product, n is the total amount of products, “condition” is 200 yuan.

C++ Definition
Function signature:
vector<int> scramble_wool(int* items, int n, int condition)

Note: please output the products in descend price order.

Python Definition
You may design your own function signature

Example 1: 
Input:
Items: [2,3,5,7,11,13,17,19,23,29,31,37,41,
        43,47,53,59,61,67,71,73,79,83,89,97,
        101,103,107,109,113,127,131,137,139,149]
n: 35
condition: 200
Output: [149 43 5 3]

Example 2:

Input:
Items: [2,3,5,7,11,13,17,19,23,29,31,37,41,
        43,47,53,59,61,67,71,73,79,83,89,97,
        101,103,107,109,113,127,131,137,139,149]
n: 35
condition: 199
Output: [149 47 3]
'''

import copy

def _scramble_wool(combs,items,condition,comb,best_diff,orig_condition):
    for i,item in enumerate(items):
        comb_cp = copy.deepcopy(comb)
        comb_cp.append(item)
        condition_cp = condition
        condition_cp -= item
        items_cp = [item for item in items[i+1:] if item <= condition_cp]
        if items_cp:
            _scramble_wool(combs,items_cp,condition_cp,comb_cp,best_diff,orig_condition)
        else:
            sum_ = sum(comb_cp)
            # 大于等于 condition 且最接近 condition 的组合是最好的
            if sum_ >= orig_condition and  sum_ - orig_condition  <= best_diff:
                best_diff = max(best_diff,sum_-orig_condition)
                combs.append(comb_cp)

import ipdb

def scramble_wool(items:list,condition:int):
# Sort items
    items = sorted(items,reverse=True)
# `combs` for all combinations to output
    combs = []
# Init `comb` and `best_diff`
    comb = []
    best_diff = condition  # 大于等于 condition 且最接近 condition 的组合是最好的
# 递归计算所有组合
    _scramble_wool(combs,items,condition,comb,best_diff,condition)
    sums = [sum(comb) for comb in combs]
    max_sums = max(sums)
    combs = [comb for sum_,comb in zip(sums,combs) if sum_==max_sums]
    print('There are [{}] different combinations, each of which sums up to [{}].'.format(len(combs),sum(combs[0])))
    return combs


if __name__=='__main__':
    items = [2,3,5,7,11,13,17,19,23,29,31,37,41,
            43,47,53,59,61,67,71,73,79,83,89,97,
            101,103,107,109,113,127,131,137,139,149]
    scramble_wool(items,200)
    scramble_wool(items,199)
