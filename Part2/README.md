## Part 2: K-means using MRJob 

### Overview 
In this part, we will use the .npy file of vector representations of words from Part 1. We first modified the format of the file, then we constructed the topic clusters using K-means algorithm. 

### Data Modification
The vector representation of words file is 1.29GB. There are a total of 537,358 vectors of length 300 in the file. As required by part 3, we need to use K-means to construct 20 clusters with indices of vectors included in each cluster. Thus, we first use np.load to load the .npy file. Then, we add the index to the end of each row of the vector and save the modified file. 

### Centroid Initialization
First, we randomly pick twenty indices. Then, we find the corresponding vectors according to the index number at the end of each row. 

### K-means Algorithms and Implementation
We use MapReduce to implement the K-means algorithm. For each iteration, the MapReduce algorithm is the following:

*	Mapper: For each line of vector representation of a word, we find the distance of that vector to the twenty centroids. Then, we find the cluster it belongs to according to the minimum distance between vector and centroids. Finally, we pass the cluster number it belongs to and a tuple with vector and its index to the combiner.

*	Combiner: For each cluster, we get several tuples passed by the mapper function. We add all the vectors together to get a sum vector and the count of how many vectors included. And we append the indices together and get a list of indices. Finally, we pass the cluster number and a corresponding tuple with the sum vector, count, and the indices list to the reducer.

*	Reducer: For each cluster, we get several tuples passed by the combiner function. We add all the sum vectors and the counts to get a total sum vector and a total count. Then, we can get the new centroid vector by calculating the mean using total sum vector divided by the total count. In addition, we concatenate all the indices list in the same cluster. Finally, we output the result twenty new centroid of clusters with the indices of vectors in it.  

*   Iteration: The above finishes one iteration of the K-means algorithm. Then, we use shell script to implement 100 iterations. It takes overnight to finish all the iterations. We find that the centroid converges at 88 iterations. 

#### Output for the next-step analysis:
*	centroid_final.txt: a text file including twenty clusters with centroid vector and corresponding vector indices included in it. 608KB
