#!/usr/bin/env bash

killall python3;
source ./venv/bin/activate;

n=32
python3 ./GenerateKeys.py $n
for i in {0..$n}; do
    echo $i
    python3 replicanetwork.py $n $i &
    sleep 1
done

python3 ./ClientMain.py $n 1 64;

#n = 4
#for i in {1..4}; do
#    echo $i
#    python3 ./ReplicaMain.py $n $i &
#    sleep 1
#done