## Deciphering 10K: A Topic Modeling Approach

Our data are 10-K reports of the US listed companies, scraped from the website of the U.S. Securities and Exchange Commission (SEC). A Form 10-K is an annual report required by  the SEC, that gives a comprehensive summary of a company's financial performance. We only use the first Item of the forms (Business) for our analysis. The data size is 2.25GB, containing 61,424 separate files from 1995 to 2008.

Usually, companies’ 10-Ks are structured in very stable patterns, which highlight the information regarding the company’s business. The salient readability of these files makes it possible for our algorithms to learn their latent topics and the relationships between companies. So we will test the following hypotheses: 

1. After converting all the words that appeared in these files into vector representations, we might be able to group the words into clusters(topics) and the weight of each word. By studying the words and their weights in each topic, we may be able to identify what are the underlying topics and compute the loadings of each file on these topics. 

2. After getting the topic loadings of each 10k file, we may able to identify similar company pairs and see why they are similar, and whether there’s any possibility of merging or acquisition.

###Part 1: Data Downloading & Preprocessing

This part is implemented in get_filling.py. 

SEC provides index files for all historical documents, including information such as the type of document, the downloading address, and CIK of the reported company. Using the index files, we first filter the 10-k documents, and then use the addresses provided to download the files. After getting the raw files, we parse the html files to text, and extract the first Item (Business) from the text.

Since the index files are organized by quarter, there are 56 index files for the period 1995-2008. So the downloading and preprocessing are naturally paralleled over the index files. Using Python multiprocessing and 20 cores on a node, the whole process finished in 8 hours.

#### Outputs:

- One txt file "CIK_date.txt" for each company and each year. All files are organized in folders by year.

###Part 2: Data Preprocessing & Word2Vec

The second step of text data preproceesing includes removing punctuations, numbers, stop-words, and changing to lowercase. For each document, the words are cleaned and collected in parallel. Then using a tool provided by the Gensim package, the words are uniquely indexed and a dictionary is formed. Based on this dictionary, we convert the documents to bag-of-words, which is also executed in parallel. Finally, using Google's pretrained word-to-vec model, we find the vector representation of each word in our dictionary, which is also executed in parallel. Using Python multiprocessing and 20 cores on a node, the whole process finished in 1 hour.

####Outputs:

- filename: pickle file that contains a list of the names of the documents
- 10k_dic: pickle file that contains a dictionary of the words and their indices. (i.e. {0:word0, 1:word1...})
- 10k_bow: pickle file that contains a list of the bag-of-words of the documents, following the order specified by filename and the indices specified by 10k_dic.
  - e.g. There are three words "apple", "orange" and "juice", two documents doc1 = "apple juice" and doc2 = "orange juice". Then filename would be [doc0, doc1], 10k_dic would be {0:"apple", 1:"orange", 2:"juice"}, 10k_bow would be [ [0, 2], [1, 2] ]. 
- vectors: saved numpy array that contains the word2vec vectors of all the words, following the order specified by 10k_dic.