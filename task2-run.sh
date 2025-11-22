#!/bin/bash
K=$1
v=$2
i=1
while :
do
	hadoop jar ./hadoop-streaming-3.1.4.jar \
    -D mapred.reduce.tasks=3 \
    -D mapred.text.key.partitioner.options=-k1 \
    -file medoids.txt \
    -file ./mapper2.py \
    -mapper ./mapper2.py $i $K \
    -file ./reducer2.py \
    -reducer ./reducer2.py \
    -input /input/Trips.txt \
    -output /output/task2-$i \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
        
    rm -f medoids1.txt
    hadoop fs -copyToLocal /output/task2-$i/part-00000 medoids1.txt
	
    seeiftrue=`python convergenceCheck.py` 
	
	if [ $seeiftrue = 1 ]
	then
		rm medoids.txt
		hadoop fs -copyToLocal /output/task2-$i/part-00000 medoids.txt
		break
	else
		rm medoids.txt
		hadoop fs -copyToLocal /output/task2-$i/part-00000 medoids.txt
	fi
    
	i=$((i+1))
    if [ $i = v]
    then
        break
    fi
done



