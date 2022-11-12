#!/bin/bash

# connects to the VM via SSH and executes given command on it
ssh -o "StrictHostKeyChecking no" -i keys/log8145-key-pair.pem ubuntu@"$1" 'bash -s' < "$2" $3 $4 > "$5" 2>&1
