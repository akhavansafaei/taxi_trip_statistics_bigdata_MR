#!/bin/bash
K=$1  # Number of clusters
V=$2  # Number of iterations
i=1

while [ $i -le $V ]
do
    hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=1 \
    -D mapred.text.key.partitioner.options=-k1 \
    -file ./mapper.py \
    -mapper "./mapper.py $i $K" \
    -file ./reducer.py \
    -reducer ./reducer.py \
    -input /Trips.txt \  # Change this to your input file location
    -output /mapreduce-output$i \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
        
    rm -f medoids1.txt
    hadoop fs -copyToLocal /mapreduce-output$i/part-00000 medoids1.txt

    # Use the latest medoids produced by the previous reduce program in the next iteration
    cp medoids1.txt medoids.txt
	
    i=$((i+1))
done
