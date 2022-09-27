# -*- coding: utf-8 -*-
"""
# Author: lixiang
# Created Time : Sat 12 Mar 2022 10:59:06 AM CST
# File Name: kdma.py
# Description:
"""
__all__ = ['MovingAverage']

class MovingAverage:
    def __init__(self, num_bin: int, window: float):
    # num_bin 必须是不小于1的整数
        assert num_bin >= 1
        self.num_bin = num_bin
        self.window = window
    # 初始化变量
        self.cur_t = 0      # 最新的价格所处的时间戳
        self.sum_T = 0      # 最新window内数据点中所有价格间的时间间隔之和
        self.n = 0          # 最新window内数据点的个数
        self.ts = []        # 最新window内数据点的时间戳列表
        self.Ts = []        # 最新window内数据点的时间间隔列表
        self.ps = []        # 最新window内数据点的价格列表
        self.ws = []        # 最新window内数据点的用于计算SMA的权重列表，w_i = window - (self.cut_t - t_i)
        self.cnts = []      # 最新window内数据点中被合并计算的数据点数量列表

    def Get(self) -> float:
    # SMA = sum(p_i*w_i)/sum(w_i)
    # 其中 w_i = window - (self.cut_t - t_i)
        sum_wp = sum([p*w for p,w in zip(self.ps,self.ws)])
        sum_w = sum(self.ws)
        return sum_wp/sum_w
        
    def Update(self, timestamp: float, value: float):
    # 记录最新的时间戳和与上个时间戳的时间间隔
        T = timestamp - self.cur_t
        self.cur_t = timestamp
    # 当加入新数据点时，如果总的时间间隔超过了window，就按FIFO剔除最早的若干数据点，直到总时间间隔小于等于window
        while self.n > 0 and self.sum_T + T > self.window:
            t0 = self.ts.pop(0)
            T0 = self.Ts.pop(0)
            p0 = self.ps.pop(0)
            w0 = self.ws.pop(0)
            self.cnts.pop(0)
            self.sum_T -= T0
            self.n -= 1
    # 如果已经达到内存上限，则找出与前一个数据点时间间隔最小的数据点，将二者的价格和权重合并存储
        if self.n == self.num_bin:
            i = argmin(self.Ts[1:]) + 1
            ti = self.ts.pop(i)
            Ti = self.Ts.pop(i)
            wi = self.ws.pop(i)
            pi = self.ps.pop(i)
            cnti = self.cnts.pop(i)
            self.n -= 1
        # update
            self.ts[i-1] = ti
            self.Ts[i-1] += Ti
            w_ = self.ws[i-1] + wi
            p_ = (self.ws[i-1]*self.ps[i-1] + wi*pi)/w_
            self.ws[i-1] = w_
            self.ps[i-1] = p_
            self.cnts[i-1] += cnti
    # 向内存中存新数据点
        self.ps.append(value)
        self.ts.append(timestamp)
        self.Ts.append(T)
        # 每加入一个新数据点，之前的每个时间点的权重都将相应减少T。若某个时间点之前被合并过，则应该减少合并数*T
        self.ws = [w - T*cnt for w,cnt in zip(self.ws,self.cnts)]
        # 新加入的时间点的权重 = window
        self.ws.append(self.window)
        self.cnts.append(1)
        self.sum_T += T
        self.n += 1
        # 保证存储的数据长度不能超过内存限制
        assert self.n <= self.num_bin

def argmin(values):
    return min(enumerate(values), key=lambda x: x[1])[0]

