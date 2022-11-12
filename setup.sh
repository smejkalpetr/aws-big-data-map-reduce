#!/bin/bash

if [ $# -eq 0 ];
then
    echo "[INFO] Starting..."

    # setup phase
    echo "[INFO] Setting up venv and installing requirements (see logs/venv_setup.log for more details)..."
    mkdir -p ./keys
    mkdir -p ./logs
    virtualenv venv > ./logs/venv_setup.log 2>&1 && \
    source venv/bin/activate > ./logs/venv_setup.log 2>&1 && \
    pip install -r requirements.txt > ./logs/venv_setup.log 2>&1;
    echo "[INFO] Done installing."

    # run phase
    echo "[INFO] Running the program..."
    python3 ./src/main.py;
    echo "[INFO] Done running."
    
    # clean phase
    echo "[INFO] Cleaning..."
    deactivate;
    rm -rf ./venv;
    # rm -rf ./keys;
    echo "[INFO] Done cleaning."

    echo "[INFO] Finished."
elif [ $# -gt 2 ];
then
    echo "$0: [INFO] Too many arguments: $@"
    exit 1
else
    if [  "$1" == "clean" ];
    then
        # cleaning utility
        echo "[INFO] Cleaning..."
        deactivate
        mkdir -p ./keys
        mkdir -p ./logs
        rm -rf ./venv
        echo "[INFO] Done cleaning."
    else
        echo "[INFO] Wrong argument."
    fi
fi