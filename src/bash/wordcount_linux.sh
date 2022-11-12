#!/bin/bash

source ~/.profile

TIMEFORMAT=%R

SUM_TOTAL_TIME=0

for i in {1..3}
  do
    TOTAL_TIME=$(
    time (
      for input in ./input/input_file*.txt
        do
          cat "$input" | tr ' ' '\n' | sort | uniq -c > /dev/null
        done
      ) 2>&1
    )

    echo "Run #${i}: The total time for all files to be processed by Linux (Wordcount) is ${TOTAL_TIME} seconds."
    SUM_TOTAL_TIME=$(echo "$SUM_TOTAL_TIME + $TOTAL_TIME" | bc)
  done

AVG=$(echo "scale=3;($SUM_TOTAL_TIME) / 3.0" | bc | awk '{printf "%f", $0}')
echo "The average time for all files to be processed by Linux (Wordcount) is ${AVG} seconds."
