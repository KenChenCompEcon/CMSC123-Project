import random
k = 20
centroid_idx = random.sample(range(530000), k)

file = open('data_modified.txt', 'w')
cent = open('centroid.txt', 'w')
f =  open('data.txt', 'r')
count = 0
for line in f:
    l = line.strip()
    l = l.split(',')
    l = l[0:len(l) - 1]
    for i in l:
        if float(i) != 0:
            if count in centroid_idx:
                temp = line.strip().split(',')
                temp = temp[0:len(temp) - 1]
                cent.write(','.join(temp) + ':' + '\n')
            count += 1
            file.write(line)
            break
f.close()
cent.close()
file.close()
