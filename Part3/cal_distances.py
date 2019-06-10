#! /usr/bin/env python
#coding=utf-8

import pickle
import threading
import numpy as np
import gc

#mu = threading.Lock()
#def write_dist(i, j, year):
#    if mu.acquire(True):
#        f = open("./distances/distances"+str(year), 'a+')
#        dist = np.linalg.norm(np.array(load[year][i][1]) - np.array(load[year][j][1]))
#        f.write(str(load[year][i][0])+','+str(load[year][j][0])+','+str(dist)+'\n')
#        f.close()
#        mu.release()
#    
#if __name__=="__main__":
#    load = {}
#    for year in range(1997, 2009):
#        with open('D:/Large Scale Data Method/Part3/loadings/loadings_byYear/document_load_' + str(year), 'rb') as f:
#            load[year] = pickle.load(f)
#    for year in range(1997, 2009):
#        thread_lst = []
#        for i in range(len(load)-1):
#            for j in range(i+1, len(load[year])):
#                thread_lst.append(threading.Thread(target = write_dist, args=(i, j, year)))
#        for t in thread_lst:
#            t.start()
#        for t in thread_lst:
#            t.join()

if __name__=="__main__":
    for year in range(1997, 2009):
        with open("document_load_" + str(year), "rb") as f:
            load = pickle.load(f)
        f = open("./distances/distances"+str(year), 'w')
        for i in range(len(load)-1):
            for j in range(i+1, len(load)):
                dist = np.linalg.norm(np.array(load[i][1]) - np.array(load[j][1]))
                f.write(str(load[i][0])+','+str(load[j][0])+','+str(dist)+'\n')
        f.close()
        del(load)
        gc.collect()
        print(str(year) + ' done')