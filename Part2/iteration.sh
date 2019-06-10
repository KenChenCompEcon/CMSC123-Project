#!/usr/bin/env bash
python MRKMeans.py data_modified.txt --c centroid_initial.txt >centroid1.txt

for iteration in $(seq 99)
do
   python MRKMeans.py data_modified.txt --c centroid$iteration.txt >centroid$[iteration + 1].txt
done
