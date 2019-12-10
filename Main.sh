#!/usr/bin/env bash

killall python3;
source ./venv/bin/activate;

n=32
python3 ./GenerateKeys.py 32
for i in {0..$n}
do
    echo $i
    python3 ./ReplicaMain.py $n $i &
    sleep 1
done
python3 ./ClientMain.py 32 1 64;

#n = 4
#for i in {1..4}; do
#    echo $i
#    python3 ./ReplicaMain.py $n $i &
#    sleep 1
#done