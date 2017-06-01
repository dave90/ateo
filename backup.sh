#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    exit 0
fi
DATE=`date +%d_%m_%Y`
N=$(basename $1)
FNAME=$DATE"_$$_backup_$N"
cp -r $1 oldresult/
mv oldresult/$N oldresult/$FNAME
FNAME=oldresult/$FNAME
for D in `ls $FNAME`;
do

    find $FNAME/$D -maxdepth 1 -type f ! -name ".out*" -delete
    rm -rf $FNAME/$D/checker
    
done

