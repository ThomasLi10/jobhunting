# -*- coding: utf-8 -*-
"""
# Author: lixiang
# Created Time : Sun 27 Feb 2022 09:37:24 AM CST
# File Name: simtrade.py
# Description:
"""

# ------------------------------ Import ------------------------------ 
import numpy as np

# ------------------------------ Sim ------------------------------ 
class Sim():
    def __init__(self,Fs,Ss):
        # args
        self.Fs = Fs
        self.Ss = Ss
        self.N = len(self.Fs)
        # key vars
        self.daily_shares = np.zeros(self.N)
        self.daily_pnls = np.zeros(self.N)
        self.target_share = 0
        self.current_share = 0

    def run(self):
        for t in range(self.N):
            self.cur_t = t
            self.trade()
            self.fill()
            self.cal_pnl()

    def fill(self):
        self.daily_shares[self.cur_t] = self.target_share
        if self.cur_t>0:
            self.current_share = self.daily_shares[self.cur_t-1] 


    def cal_pnl(self):
        if self.cur_t>0:
            self.daily_pnls[self.cur_t] = (self.Ss[self.cur_t] - self.Ss[self.cur_t-1])\
                    *self.current_share
        
    @property
    def total_pnl(self):
        return np.sum(self.daily_pnls)

    def trade(self):
        # Your strategy
        pass

            
class SimB(Sim):
    def trade(self):
        self.target_share = self.Fs[self.cur_t]
    

# ------------------------------ Run ------------------------------ 
if __name__=='__main__':
    model = SimB([-1,1,-1],[2,2.1,1.9])
    model.run()
    print(model.daily_pnls)
    print(model.total_pnl)
