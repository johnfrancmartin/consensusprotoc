#!/usr/bin/env bash

killall python3;
source ./venv/bin/activate;

n=8
python3 ./GenerateKeys.py 8
for i in {1..8};
do
    echo ${i}
    python3 ./ReplicaMain.py ${n} ${i} &
    sleep 1
done
python3 ./ClientMain.py ${n} 1 2048;