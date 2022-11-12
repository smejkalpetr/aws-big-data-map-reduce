#!/bin/bash

> $2

scp -i ./keys/log8145-key-pair.pem ./src/map_reduce/input.txt ubuntu@$1:~ >> $2 2>&1
echo "Social Network Problem's input data successfully copied to remote." >> $2

scp -i ./keys/log8145-key-pair.pem ./src/pyt/mapper.py ubuntu@$1:~ >> $2 2>&1
echo "Social Network Problem's mapper.py successfully copied to remote." >> $2

scp -i ./keys/log8145-key-pair.pem ./src/pyt/reducer.py ubuntu@$1:~ >> $2 2>&1
echo "Social Network Problem's reducer.py successfully copied to remote." >> $2
