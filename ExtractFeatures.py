# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 04:44:25 2016

@author: Ray

how to select feature and output

example:
scale = 6
lookback = 4
output = 6

-128,-96,-64,-32,-64,-48,-32,-16,-32,-24,-16,-8,-16,-12,-8,-4,-8,-6,-4,-2,-4,-3,-2,-1,0,1,2,3,4,5

"""

import math
import numpy as np

def loadOhlc(path):
    arr = np.loadtxt(path, skiprows=1, usecols=[1,2,3,4,5],delimiter=',')
    return arr
    
def getOffset(lookback, scale, output):
    a = np.arange((-1)*lookback, 0, 1)
    o = np.arange(output)
    r = np.concatenate([a,o])
    b = np.arange(1, scale)
    for i in b:
        c = int(math.pow(2, i))*a
        r = np.concatenate([c,r])
    return r

def getIndexArray(pos, lookback, scale, output):
    return pos + getOffset(lookback, scale, output)
    
def main(inpath, outpath, lookback, scale, output):
    samples = []    
    arr = loadOhlc(inpath)
    # avg_price = (O + H + L + C)/4
    avg_price = (arr[:,0] + arr[:,1] + arr[:,2] + arr[:,3])/4
    # normalize    
    avg_price = avg_price / avg_price.max();
    pos = lookback*int(math.pow(2,scale-1)) + 1
    while pos < avg_price.size - output:
        index_array = getIndexArray(pos, lookback, scale, output)
        if index_array[0] < 0:
            continue
        sample = avg_price[index_array]
        samples.append(sample)        
        pos = pos + 1
    np.savetxt(outpath, samples, fmt='%.2e', delimiter=',')
    return np.array(samples)
    
        
        
        
        