import multiprocessing
import SVD_Class
import gensim
import pickle
import os
import gc
import numpy as np
from time import time

# Define the svd job for each topic, and export the topic loadings & document loadings
def svd(d, bow, topic, topic_idx, year):
    print('Topic {:.0f} svd starting'.format(topic_idx))
    start = time()
    svd_instance = SVD_Class.SVD_Textual_Factors(bow, topic)
    topic_loading = svd_instance.topic_loading()
    document_loading = svd_instance.document_loading()
    with open(d + '/loadings/topic_loading_' + str(year) + '_' + str(topic_idx), 'wb') as f:
        pickle.dump(topic_loading, f)
    with open(d + '/loadings/document_loading_'+ str(year) + '_' + str(topic_idx), 'wb') as f:
        pickle.dump(document_loading, f)
    del(svd_instance)
    gc.collect()
    print("Task {:0f} took {:2f} seconds.".format(topic_idx, time()-start))

# Run the jobs in the main environment
if __name__ == "__main__":
    # Load all the pre-calculated results
    with open('clusters', 'rb') as f:
        clusters = pickle.load(f)
    with open('./10k_bow', 'rb') as f:
        bow = pickle.load(f)
    with open('../Part1/filenames', 'rb') as f:
        filenames = pickle.load(f)
        
    k = len(clusters)
    d = os.getcwd()
    cutoff = []; count = 1; year = '1995'
    for i in range(1,len(filenames)):
        if filenames[i][6:10] == year:
            count +=1
        else:
            cutoff.append((count, int(year)))
            year = filenames[i][6:10]
            count = 1
    cutoff.append((count, int(year)))
            
    start_time = time()
    p = multiprocessing.Pool(3)
    for i in range(1, 20):
        topic = clusters[i]
        p.apply_async(func=svd, args = (d, bow, topic, i))
    print("Processes starting...")
    p.close()
    p.join()
    print("The entire process job took {:2f} seconds".format(time()-start_time))