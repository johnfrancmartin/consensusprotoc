#!/usr/bin/env bash

killall python3;
source ./venv/bin/activate;

n=64
python3 ./GenerateKeys.py 64
for i in {1..64};
do
    echo ${i}
    python3 ./ReplicaMain.py ${n} ${i} &
    sleep 1
done
python3 ./ClientMain.py ${n} 1 2048;