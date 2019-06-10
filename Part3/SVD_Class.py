import numpy as np
import gensim
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FormatStrFormatter
import os
import math
import scipy.linalg as sci
import timeit

class SVD_Textual_Factors:

    def __init__(self, bow, topic = -1):
        corpus_dict = []
        for i in range (0, len(bow)):
            corpus_dict.append({key: value for key, value in bow[i]})
        self.corpus_dict = corpus_dict
        if (topic!=-1).all():
            self.topic = topic
            self.term_document_frequency_matrix = self.document_term_matrix(topic)
            self.t_ldings, self.sv, self.v_ldings = sci.svd(self.term_document_frequency_matrix, 
                                                            full_matrices = False)

    def SVD_topic(self, topic): # topic：a list of word keys
        self.topic = topic
        self.term_document_frequency_matrix = document_term_matrix(self, topic)
        self.t_ldings, self.sv, self.v_ldings = sci.svd(self.term_document_frequency_matrix, 
                                                        full_matrices = True)
        
    def find_topic(self, concept, clusters):
        words = []
        for topic in clusters:
            if ((np.asarray(topic) == concept).any()):
                words = topic
                break
        return words
    
    def word_documents_freq(self, word_id):
        word_counts_over_doc = np.zeros(shape = (1,self.n), dtype= np.int64) # 1 x n array n - number of documents
        for doc_num in range (0, self.n):
                try: 
                    word_counts_over_doc[0][doc_num] = self.corpus_dict[doc_num][word_id]
                except KeyError:
                    continue 
        return word_counts_over_doc

    # m - number of words in topic
    # n - number of documents in corpus
    # A ~ R^(m x n) matrix w_(i,j) is count of word i in document j
    def document_term_matrix(self, topic):
        #Getting Dimensions of Matrix
        self.n = len(self.corpus_dict) #n is number of documents
        self.m = len(self.topic) # m is number of words (size of vocabulary)
        #Instantiating Term-Document Frequency Matrix
        matrix = np.zeros(shape = (self.m, self.n), dtype= np.int64)   
            #filling_matrix
        for m_i in range (0,self.m):
                matrix[m_i] = self.word_documents_freq(topic[m_i])
        return matrix

    def topic_loading(self):
        return self.t_ldings[:,0]

    def document_loading(self):
        return self.v_ldings[0,:] 