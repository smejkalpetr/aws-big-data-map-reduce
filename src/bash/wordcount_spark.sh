#!/bin/bash

source ~/.profile

TIMEFORMAT=%R

scp myfile.txt -i ./keys/log8145-key-pair.pem ./src/pyt/wordcount_spark.py ubuntu@$1:~

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
      spark-shell -i ~/wordcount_spark.py > /dev/null 2>&1

      ) 2>&1
    )

    SUM_TOTAL_TIME=$(echo "$SUM_TOTAL_TIME + $TOTAL_TIME" | bc)
    echo "Run #${i}: The total time for all files to be processed by Spark (Wordcount) is ${TOTAL_TIME} seconds."
  done

AVG=$(echo "scale=3;($SUM_TOTAL_TIME) / 3.0" | bc | awk '{printf "%f", $0}')
echo "The average time for all files to be processed by Spark (Wordcount) is ${AVG} seconds."
