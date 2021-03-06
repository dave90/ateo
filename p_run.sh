#!/bin/bash

if [ "$#" -ne 3 ]
then
    echo "Wrong arguments. Please specify: system, folder and max number of rules to annotate"
    exit 1
fi


SYSTEM=$1
FOLDER=$2
IDLV_STATS="idlv-stats-portable/idlv"
MAX_RULE=$3

for D in `ls $FOLDER`;
do
    echo "screen -d -m bash -c \"./run.sh $SYSTEM $FOLDER/$D $MAX_RULE\""
    screen -d -m bash -c "./run.sh $SYSTEM $FOLDER/$D $MAX_RULE"
    echo "RUN $D"
    `sleep 2`
done

