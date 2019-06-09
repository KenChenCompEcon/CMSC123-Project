import os
import re
from gensim import corpora, models
from nltk.corpus import stopwords
import multiprocessing
import pickle
import numpy as np

#set the directory containing 10k files and the path of pretrained word2vec model
wdir = './10k/'
w2v_path = 'GoogleNews-vectors-negative300.bin'

def hasNumbers(inputString):
    '''check if there's any number in a string'''
    return any(char.isdigit() for char in inputString)
    
def clean_punc(s):
    '''remove the punctuations in a string'''
    return re.sub("[^A-Za-z]", "", s).lower().strip()

#set the stop words    
stop_words = stopwords.words('english')
stop_words.append('PAGE')

def tokenize(filename):
    '''open a 10k file, remove punctuations, numbers, stop-words, change to lowercase, return the cleaned list of words'''
    openfile = open(filename, 'r', errors='ignore')
    raw = openfile.read()
    openfile.close()
    words = raw.split()
    words = [clean_punc(word) for word in words]
    words = [word.lower() for word in words if word and word not in stop_words and not hasNumbers(word)]
    return words

#collect the filenames of all 10k files in a list
files = []
for year in os.listdir(wdir):
    if os.path.isdir(wdir+year):
        for file in os.listdir(wdir+year):
            files.append(wdir + year + '/' + file)
pool = multiprocessing.Pool()
#pool over the list of filenames
texts = pool.map(tokenize, files)
#form a dictionary of all index:word pairs
dic = corpora.Dictionary(texts)
#form the bag-of-words for all documents
corpus = pool.map(dic.doc2bow, texts)

#save filenames, dictionary, bow
with open('filenames', 'wb') as f:
    pickle.dump(files, f)        
dic.save('10k_dic')
with open('10k_bow', 'wb') as f:
   pickle.dump(corpus, f)

#load the word2vec model   
w2v_model = models.KeyedVectors.load_word2vec_format(w2v_path, binary=True)

#find the vector representation of a word
def w2v(item):
    global w2v_model
    try:
        vec = w2v_model[item[1]]
    except:
        #words that are not in the model has all-zero vector representation
        vec = np.zeros(300)
    return vec

#map over the dictionary
pool = multiprocessing.Pool()
vectors = pool.map(w2v, dic.items())
#save the vectors as numpy array
vectors = np.array(vectors)
np.save('vectors', vectors)