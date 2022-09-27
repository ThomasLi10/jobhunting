# -*- coding: utf-8 -*-
"""
# Author: lixiang
# Created Time : Sun 27 Feb 2022 09:19:51 AM CST
# File Name: opt.py
# Description:
"""

# ------------------------------ Import ------------------------------ 
import numpy as np

# ------------------------------ Optimizer ------------------------------ 
class Optimizer():
    def __init__(self,y,x1,x2,lambda_,init_b1=0,init_b2=0,n_iter=10):
        self.y = y
        self.x1 = x1
        self.x2 = x2
        self.lambda_ = lambda_
        self.init_b1 = init_b1
        self.init_b2 = init_b2
        self.b1 = init_b1
        self.b2 = init_b2
        self.n_iter = n_iter

    def update(self,x1,x2,b2):
        y = self.y - b2*x2
        return np.sign(x1*y)*np.max([0,np.abs(y)-self.lambda_])/x1**2
    
    def update_b1(self):
        return self.update(self.x1,self.x2,self.b2)

    def update_b2(self):
        return self.update(self.x2,self.x1,self.b1)
    
    def run(self):
        for i in range(self.n_iter):
            print('Iter {}'.format(i), end='')
            self.b1 = self.update_b1()
            self.b2 = self.update_b2()
            print(' | b1 = {:.4f} , b2 = {:.4f}'.format(self.b1,self.b2))

# ------------------------------ Run ------------------------------ 
if __name__=='__main__':
    model = Optimizer(1,2,3,0.1)
    model.run()
