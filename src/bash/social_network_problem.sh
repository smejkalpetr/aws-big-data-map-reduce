#!/bin/bash

source ~/.profile

TIMEFORMAT=%R

# install utils
sudo apt install dos2unix > /dev/null 2>&1

# convert files from dos to unix format
dos2unix mapper.py > /dev/null 2>&1
dos2unix reducer.py > /dev/null 2>&1

TOTAL_TIME=$(
    time (
        # start dfs and yarn
        /usr/local/hadoop-3.3.1/sbin/start-dfs.sh > /dev/null 2>&1
        /usr/local/hadoop-3.3.1/sbin/start-yarn.sh > /dev/null 2>&1

        # create input inside hdfs
        hdfs dfs -mkdir -p /user/hadoop/input_social > /dev/null 2>&1

        # put data to hdfs
        hdfs dfs -put input.txt /user/hadoop/input_social/ > /dev/null 2>&1

        # run
        mapred streaming -input /user/hadoop/input_social/input.txt -output output_social -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py > /dev/null 2>&1
      ) 2>&1
    )

echo "It took ${TOTAL_TIME} seconds to solve the Social Network Problem using map reduce."
echo ''

# list the result
hdfs dfs -cat /user/ubuntu/output_social/part-00000