import numpy as np
vectors = np.load('vectors.npy')

file = open('data.txt', 'w')
index = 0
for pt in vectors:
    file.write(','.join(list(map(str, pt))) + ',' + str(index) + '\n')
    index += 1
file.close()
