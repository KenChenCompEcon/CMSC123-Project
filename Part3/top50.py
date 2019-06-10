# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 22:56:27 2019

@author: Ken CHEN
"""

from mrjob.job import MRJob 
from mrjob.step import MRStep
import heapq
import re

WORD_RE = re.compile(r"[\w]+")

class shortestPair(MRJob):
    
    def mapper_init(self):
        self.h = [(-100, -1, -1)]*50
        heapq.heapify(self.h)
        
    def mapper(self, _, line):
        val = line.strip().split(',')
        val = (-float(val[2]), int(val[0]), int(val[1]))
        if val[0] >= self.h[0][0]:
            heapq.heapreplace(self.h, val)
            
    def mapper_final(self):
        for i in range(50):
            yield heapq.heappop(self.h), None
    
    def reducer_init(self):
        self.h = [(-100, -1, -1)]*50
        heapq.heapify(self.h)
    
    def reducer(self, pair, _):
        if pair[0]>=self.h[0][0]:
            heapq.heapreplace(self.h, tuple(pair))
    
    def reducer_final(self):
        for i in range(50):
            yield heapq.heappop(self.h), ''

if __name__=='__main__':
	shortestPair.run()
