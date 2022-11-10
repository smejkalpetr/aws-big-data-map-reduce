#!/bin/bash

ssh -o "StrictHostKeyChecking no" -i keys/log8145-key-pair.pem ubuntu@"$1" 'bash -s' < src/bash/vm_setup.sh > ./logs/ssh_setup.log 2>&1
