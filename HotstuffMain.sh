#!/usr/bin/env bash

killall python3;
source ./venv/bin/activate;

n=32
python3 ./GenerateKeys.py 32

python3 ./HotstuffReplicaMain.py 4 1 &
python3 ./HotstuffReplicaMain.py 4 2 &
python3 ./HotstuffReplicaMain.py 4 3 &
python3 ./HotstuffReplicaMain.py 4 4 &
python3 ./ClientMain.py ${n} 1 512;


#for i in {1..32};
#do
#    echo ${i}
#    python3 ./ReplicaMain.py ${n} ${i} &
#    sleep 1
#done
#python3 ./ClientMain.py ${n} 1 2048;