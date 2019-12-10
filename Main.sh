#!/usr/bin/env bash

killall python3;
source ./venv/bin/activate;
#pip list;
python3 ./GenerateKeys.py 5;
python3 ./ReplicaMain.py 5 1 &
sleep 1
python3 ./ReplicaMain.py 5 2 &
sleep 1
python3 ./ReplicaMain.py 5 3 &
sleep 1
python3 ./ReplicaMain.py 5 4 &
sleep 1
python3 ./ReplicaMain.py 5 5;
#sleep 1
#python3 ./ClientMain.py 5 3 2048;

#n = 4
#for i in {1..4}; do
#    echo $i
#    python3 ./ReplicaMain.py $n $i &
#    sleep 1
#done