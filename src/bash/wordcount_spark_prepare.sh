#!/bin/bash

> $2

scp -i ./keys/log8145-key-pair.pem ./src/pyt/wordcount_spark.py ubuntu@$1:~ >> $2 2>&1
echo "Spark's solution file successfully copied to remote." >> $2
