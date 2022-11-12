#!/bin/bash

source ~/.profile

TIMEFORMAT=%R

SUM_TOTAL_TIME=0

for i in {1..3}
  do
    TOTAL_TIME=$(
    time (
      # start dfs and yarn
      /usr/local/hadoop-3.3.1/sbin/start-dfs.sh > /dev/null 2>&1
      /usr/local/hadoop-3.3.1/sbin/start-yarn.sh > /dev/null 2>&1

      # create input inside hdfs
      hdfs dfs -mkdir -p /user/hadoop/input > /dev/null 2>&1

      # copy all input files to hdfs
      for input in ./input/input_file*.txt
        do
          hdfs dfs -put $input /user/hadoop/input/ > /dev/null 2>&1
        done

      # run wordcount
      hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.1.jar wordcount /user/hadoop/input/ /user/hadoop/output${i}/ > /dev/null 2>&1

      # list all results
      #hdfs dfs -ls /user/hadoop/output

      # list content of the result
      #$ hdfs dfs -cat /user/hadoop/output/part-r-00000
      ) 2>&1
    )

    echo "Run #${i}: The total time for all files to be processed by Hadoop (Wordcount) is ${TOTAL_TIME} seconds."
    SUM_TOTAL_TIME=$(echo "$SUM_TOTAL_TIME + $TOTAL_TIME" | bc)
  done

AVG=$(echo "scale=3;($SUM_TOTAL_TIME) / 3.0" | bc | awk '{printf "%f", $0}')
echo "The average time for all files to be processed by Hadoop (Wordcount) is ${AVG} seconds."
