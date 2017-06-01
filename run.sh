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

./analytic.py $IDLV_STATS $FOLDER $MAX_RULE
./annotator.py $FOLDER
./runner.py $SYSTEM $FOLDER
./stats.py $FOLDER
