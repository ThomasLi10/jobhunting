# -*- coding: utf-8 -*-
"""
# Author: lixiang
# Created Time : Sun 27 Feb 2022 10:17:53 AM CST
# File Name: avg.hold.day.py
# Description:
"""

# ------------------------------ Import ------------------------------ 
import numpy as np

# ------------------------------ SimA ------------------------------ 
class SimA():
    def __init__(self,Fs):
        # args
        self.Fs = np.array(Fs)
        self.N = len(self.Fs)
        # key vars
        self.holding_days = np.zeros(self.N)
        self.hedged = np.full(self.N,np.nan)

    def run(self):
        for t in range(self.N):
            self.holding_days[:t][self.hedged[:t]!=1] += 1
            self.hedged[t] = 0
            if t > 0:
                # 找最近一个没有hedged且信号相反的天
                idx = np.where(self.hedged[:t-1]==0)[0]
                if len(idx)>0:
                    idx2 = np.where(self.Fs[idx]==-self.Fs[t])[0]
                    # 先进先出
                    self.hedged[idx[idx2]] = 1

    @property
    def avg_holding_day(self):
        return np.mean(self.holding_days[:-1])




# ------------------------------ Run ------------------------------ 
if __name__=='__main__':
    model = SimA([-1,-1,1,-1,1])
    model.run()
    print(model.holding_days)
    print(model.avg_holding_day)
