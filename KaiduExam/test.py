# -*- coding: utf-8 -*-
"""
# Author: lixiang
# Created Time : Sat 12 Mar 2022 11:45:39 AM CST
# File Name: test.py
# Description:
"""

# ----------------------- Import ----------------------- 
from kdma import MovingAverage
import numpy as np
import pandas as pd
import time

# ----------------------- Functions ----------------------- 
def gen_flows(N,mu=0.0,sigma=0.001):
    '''
    构建时间序列及价格序列作为数据流
    '''
    np.random.seed(10)
    ts = np.cumsum(np.exp(np.random.randn(N))**2)
    ps = 10*np.cumprod(1+np.random.normal(mu,sigma,N))
    return ts,ps

def cal_ma(num_bin,window,ts,ps):
    '''
    计算数据流的平均价格
    '''
    MA = MovingAverage(num_bin,window)
    ma_ps = []
    for t,p in zip(ts,ps):
        MA.Update(t,p)
        ap = MA.Get()
        ma_ps.append(ap)
    return pd.DataFrame({'Price':ps,'MA':ma_ps},index=ts)

# ----------------------- Test ----------------------- 
if __name__=='__main__':
    # 参数
    N = 100000
    num_bin = 15
    window = 30
    # 长度为100000的数据流
    ts,ps = gen_flows(N)
    # 内存无穷大时“准确”的平均价格
    t1 = time.time()
    ma0 = cal_ma(np.inf,window,ts,ps)
    t2 = time.time()
    # 内存受限时“准确”的平均价格
    ma = cal_ma(num_bin,window,ts,ps)
    t3 = time.time()
    # 运行效率
    print('- 在内存大小为 o({}) 时，处理长度为 {} 的数据流，用时{:.2f}秒。'.format(np.inf,N,t2-t1))
    print('  在内存大小为 o({}) 时，处理长度为 {} 的数据流，用时{:.2f}秒。'.format(num_bin,N,t2-t1))
    # 二者差距对比
    print('- 上述二者计算所得 平均价格差值/原价格 统计分布如下：')
    print(((ma-ma0)['MA']/ma['Price']).describe())
    
