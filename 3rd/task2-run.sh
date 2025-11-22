#!/bin/bash

# Specify the number of iterations (V), convergence threshold (THRESHOLD), and the number of clusters (k)
V=$1
k=$2  # The number of clusters
THRESHOLD=$3
i=1
converged=0  # Initialize the convergence flag to 0 (not converged)

while [ $i -le $V ] && [ $converged -eq 0 ]
do
    # Run the MapReduce job with the specified parameters
    hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=1 \
    -D mapred.text.key.partitioner.options=-k1 \
    -D convergence.threshold=$THRESHOLD \
    -D num.clusters=$k \  # Pass the number of clusters (k) as a configuration parameter
    -file medoids.txt \
    -file ./pam_mapper.py \
    -mapper "python pam_mapper.py $i $k" \
    -file ./pam_reducer.py \
    -reducer "python pam_reducer.py $THRESHOLD" \  # Pass the convergence threshold as an argument to the reducer
    -input /dataset.txt \
    -output /mapreduce-output$i \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

    rm -f medoids.txt
    hadoop fs -copyToLocal /mapreduce-output$i/part-00000 medoids.txt

    # Check if convergence flag exists (CONVERGED)
    seeifconverged=`cat medoids.txt | grep CONVERGED`
    
    if [ -n "$seeifconverged" ]
    then
        converged=1  # Set the convergence flag to 1 (converged)
    fi

    i=$((i+1))
done

# Copy the final output to /output/task2
hadoop fs -copyToLocal /mapreduce-output$i /output/task2
