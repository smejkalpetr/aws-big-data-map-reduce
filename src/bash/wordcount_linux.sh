#!/bin/bash

for input in ./input/input_file*.txt
  do
    chmod +x "$input"
    echo "File name: ${input}"
    time for i in {1..3};
      do
        time cat "$input" | tr ' ' '\n' | sort | uniq -c > /dev/null
      done
  done
