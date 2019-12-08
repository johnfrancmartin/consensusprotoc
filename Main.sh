#!/usr/bin/env bash

killall python
killall python3
#source ./venv/bin/activate;
pip list;
python3 ./CreateBLS.py 2 4;
#python3 ./ReplicaMain.py 4 1 &
#sleep 1
#python3 ./ReplicaMain.py 4 2 &
#sleep 1
#python3 ./ReplicaMain.py 4 3 &
#sleep 1
#python3 ./ReplicaMain.py 4 4 &

n = 4
for i in {1..$n+1}; do
    echo $i
    python3 ./ReplicaMain.py $n $i &
    sleep 1
done