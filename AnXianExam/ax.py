# -*- coding: utf-8 -*-
"""
# Author: lixiang
# Created Time : Sun 20 Mar 2022 09:59:42 PM CST
# File Name: ax.py
# Description:
"""

# ========================== Import ========================== 
import numpy as np
import json
import re


# ========================== parse ========================== 
def find_all(sub,s):
    return [(m.start(),m.end()) for m in re.finditer(sub, s)]

class JsonParser():
    def __init__(self,s,input):
        self.IN = input
        self.s = s
        self.rd = json.loads(s)
        self.rfs = self.rd['functions']
        self.rvs = self.rd['values']
        # memory
        self.mem = {}

    def __getitem__(self,var):
        return self.mem[var]
    

    def run(self):
        for rf,expr in self.rfs.items():
            self.cal_expr(expr)

        for rv,exprs in self.rvs.items():
            if isinstance(exprs,str): 
                self.mem[rv] = self.cal_numpy_expr(self.search_functions(exprs))
            elif isinstance(exprs,list): 

                self.mem[rv] = [self.cal_numpy_expr(self.search_functions(expr)) for expr in exprs]
        
        return {v:self.mem[v] for v in self.rvs}

    def cal_expr(self,expr):
        while True:
            status = 0
            for f,s in self.rfs.items():
                if f not in self.mem:
                    if self.has_functions(s):
                        stauts = 1
                        if f in expr:
                            v = self.cal_expr(s)
                    else:
                        self.mem[f] = self.cal_numpy_expr(s)
            if status == 0:
                break

    def cal_numpy_expr(self,expr):
        for f in self.mem:
            exec('{0}=self.mem[\'{0}\']'.format(f))
        for k in np.__dict__:
            if k in expr:
                idxs = find_all(k,expr)
                if callable(np.__dict__[k]):
                    for i in idxs:
                        if len(expr) > i[1] and expr[i[1]].isalpha():
                            pass
                        else:
                            if len(expr) > i[1] and expr[i[1]]=='(':
                                expr = expr.replace(k,'np.{}'.format(k))
                            elif len(expr) == i[1] or expr[i[1]]!='(':
                                expr = expr.replace(k,'np.{}(self.IN)'.format(k))
                else:
                    for i in idxs:
                        if len(expr) > i[1] and expr[i[1]].isalpha():
                            pass
                        else:
                            expr = expr.replace(k,'np.{}'.format(k))

        return eval(expr)


    def has_functions(self,s):
        return any(k in s and k not in self.mem for k in self.rfs)


    def search_functions(self,s):
        while True:
            status = 0
            for k,expr in self.rfs.items():
                if k in s and k not in self.mem:
                    status = 1
                    s = s.replace(k,expr)
            if status == 0:
                break
        return s



def parse(json_string: str, input):
    parser = JsonParser(json_string,input)
    return parser.run()



# ========================== Test ========================== 
if __name__=='__main__':
    input = np.random.rand(10)
    result = parse(json_string, input)
