#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 0
fi
for D in `ls $1`;
do

    ./backup.sh $1/$D
    
done

