#!/bin/bash
if [ $# -ne 2 ]
    then
        echo "Script takes 2 args, host ip address and port number"
        exit 1
fi

scan_dir="scans_`date +%Y%m%d`"
count=0
host=$1
port=$2

if [ -d $scan_dir ]
    then
        if [ -a counter ]
            then
                count=$(cat counter)
        fi
else
    mkdir $scan_dir
    echo $count > counter
fi

python3 scanner_server.py $host $port $scan_dir $count
