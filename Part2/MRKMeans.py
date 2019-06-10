from mrjob.job import MRJob
import mrjob
import numpy as np
import os
from mr3px.csvprotocol import CsvProtocol

class MRKMeans(MRJob):
    SORT_VALUES = True

    OUTPUT_PROTOCOL = mrjob.protocol.RawProtocol
    def dist_vec(self,v1,v2):
        #calculate the distance between two vectors
        return np.linalg.norm(np.array(v1) - np.array(v2))
    
    def configure_args(self):
        super(MRKMeans, self).configure_args()
        #the line below define that the file following the --c option is the centroid and is loadable
        self.add_file_arg('--c')

    def get_centroids(self):
        """
        Definition : extracts centroids from the centroids file define after --c flag
        Out : Return the list of centroids
        """
        # self.options.c is the name of the file following --c option
        f = open(self.options.c,'r')
        centroids=[]
        for line in f.readlines():
            #print(line)
            line = line.strip()
            if line:
                line = line.split(':')[0]
                centroids.append(list(map(float, line.split(','))))
        f.close()
        # print(centroids)
        return centroids
    
    def mapper(self, _, lines):
        """
        Definition : Mapper take centroids extract form get_centroids() and the point cloud and for each point, calculate the distance to the centroids, find the mininum of it
        Out : yield the point and the index with it's class
        """
        centroids = self.get_centroids()
        lines = lines.strip()
        lines = list(map(float, lines.split(',')))
        point = lines[0:len(lines) - 1]
        index = int(lines[-1])
        min_dist = 100000000.0
        classe = 0
        #print(centroids)
        #iterate over the centroids (Here we know that we are doing a 20 means)
        for i in range(20):
            dist = self.dist_vec(point, centroids[i])
            if dist < min_dist:
                min_dist = dist
                classe = i
        yield classe, (point, index)
    
    def combiner(self, k, v):
        """
        Definition : Calculate for each class, at the end of the mapper, before reducer, the medium point of each class
        Out: return for each class, the centroids for each mapper, and the list of index
        """
        count = 0
        index_lst = []
        vector = list(v)
        sum_lst = np.zeros(len(vector[0][0]))
        for t in vector:
            point = t[0]
            index_lst.append(t[1])
            count += 1
            sum_lst += np.array(point)
        yield k, (list(sum_lst), count, index_lst)

    def reducer(self, k, v):
        """
        Definition : for each class, get all the tmp centroids from each combiner and calculate the new centroids and the index inside the cluster.
        """
        # k is class and v are medium points linked to the class
        count = 0
        index_lst = []
        vector = list(v)
        sum_lst = np.zeros(len(vector[0][0]))
        #f = open(d + '/centroids.txt', 'a')
        for t in vector:
            index_lst += t[2]
            count += t[1]
            sum_lst += np.array(t[0])
        cent = list(sum_lst / count)
        centroid_lst = ','.join(list(map(str, cent)))
        index_lst = ','.join(list(map(str, index_lst)))
        print(centroid_lst + ":" + index_lst + '\n')
        #f.write(str(sum_x/count) + "," + str(sum_y/count) + ":" + index_lst + '\n')
if __name__ == '__main__':
    d = os.getcwd()
    MRKMeans.run()