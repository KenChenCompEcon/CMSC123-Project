## Part 3: Singular Vector Decomposition + Loadings

### Overview of Part 3
In this part, we will take advantage of the ‘bag of words’ from Part 1 and the ‘topic clusters’ we got from part 2. Frequency matrices were constructed by using these pre-processed documents, and then we were able to implement Singular Vector Decomposition on these matrices, which implied what are the most important words for each topic, and how much does each document load on these topics respectively. So these were the hypotheses underneath our analysis.

### Pre-processed Data
The ‘bag of words’ file is 612MB, and the ‘topic clusters’ is 301KB, both of which are saved in binary formats. The ‘bag of words’ contains a list of 61,424 sub-lists, each representing the words count in each document. The ‘topic clusters’ is a list of 20 sub-lists, each records the word composition of that topic. Purposefully, I’ve deleted topics that contain too few or too many words.

### Algorithms and Implementation
*	The magic we are going to play here is the singular value decomposition. It is known as a factorization of a matrix of any size into single vectors. This is somehow similar to the concept of Principal Component Analysis. We can get vectors of loadings that illustrate row or column importance. By obtaining the first columns of U and V, we can see which rows and columns are contribute most to the original matrix. 
![svd](https://github.com/KenChenCompEcon/CMSC123-Project/blob/master/Part3/SVD.png?raw=true)

*	Extracting the information from the two documents, we can then build matrices of such type. And these matrices are the ones we will decompose. The first column of U are the word loadings of a topic, and the first column of V are the document loadings on a topic.
![frequency](https://github.com/KenChenCompEcon/CMSC123-Project/blob/master/Part3/Frequency%20Matrix.png?raw=true)

*	For the best of our knowledge, we are unable to implement the decomposition of a matrix in a parallel fashion and took the advantage of big-data paralleled frameworks like MapReduce or MPI. But the decompositions of matrices of different topics are naturally parallelizable. So we decided to use the Python Multiprocessing to exploit the multicores of the computer. Furthermore, since the entire process is prohibitively memory consuming, we’ve requested a 8-core cluster of 30GB memory space on Google Cloud. The entire process took 2,785 seconds on google cloud.

### Word Loadings and Document Loadings
*	We can directly get the word loadings from the previous step. Word clouds can be constructed from these vectors, where loadings can be interpreted as word frequencies.
*	By aggregating the document loadings, we can get a topic loading vector on the 12 topics for each document. The aggregation is conducted by year, and then we paired up all the document topic loadings, computing their distances and screen out the 50 pairs with the shortest distances. The computation of paired-distances is massive. We planned to use multithreading framework, but the parallel programming did not seem a good compensation for the overheads. These by-year distances altogether form an 8.12GB file. Then we fed these distances for a MapReduce TopK alogorithm, the 50 closest pairs were found for each year.

#### Output for the next-step analysis:
*	Word loadings on the 12 topics, 268KB
*	Paired-up distances for each year: 8.12GB
*	Closest pairs for each year: 128KB
