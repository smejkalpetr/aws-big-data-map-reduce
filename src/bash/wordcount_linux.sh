#!/bin/bash

TIMEFORMAT=%R

for input in ./input/input_file*.txt
  do
    chmod +x "$input"

    TOTAL_TIME=$(
      time (for i in {1..3}
        do
          cat "$input" | tr ' ' '\n' | sort | uniq -c > /dev/null
        done) 2>&1
      )

    RESULT=$(echo "scale=3;(${TOTAL_TIME})/3" | bc)
    echo "Average real time for file ${input} is ${RESULT} seconds."
  done
