#!/bin/bash

mkdir -p input

FINAL_URL=$(curl -Ls -o /dev/null -w %{url_effective} "$1")
curl "$FINAL_URL" > ./input/"$2"
