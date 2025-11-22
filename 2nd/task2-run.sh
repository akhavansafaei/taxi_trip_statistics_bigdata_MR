#!/bin/bash
K=$1  # Number of clusters
V=$2  # Number of iterations

# Initial MapReduce job for the first iteration
hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \  # Set the number of reducers
    -D mapred.text.key.partitioner.options=-k1 \
    -file ./pam_mapper.py \
    -mapper "./pam_mapper.py 1 $K" \
    -file ./pam_reducer.py \
    -reducer ./pam_reducer.py \
    -input /input/Trips.txt \  # Change this to your input file location
    -output /output/task2-1 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

# Use the latest medoids produced by the previous reduce program in the next iteration
cp /output/task2-1/part-00000 medoids.txt

i=2  # Start from the second iteration

while [ $i -le $V ]
do
    hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \  # Set the number of reducers
    -D mapred.text.key.partitioner.options=-k1 \
    -file medoids.txt \  # Use the latest medoids
    -file ./pam_mapper.py \
    -mapper "./pam_mapper.py $i $K" \
    -file ./pam_reducer.py \
    -reducer ./pam_reducer.py \
    -input /input/Trips.txt \  # Change this to your input file location
    -output /output/task2-$i \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
        
    # Use the latest medoids produced by the previous reduce program in the next iteration
    cp /output/task2-$i/part-00000 medoids.txt
	
    i=$((i+1))
done
