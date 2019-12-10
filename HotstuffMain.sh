#!/usr/bin/env bash

killall python3;
source ./venv/bin/activate;

n=4
python3 ./GenerateKeys.py 4

python3 ./HotstuffReplicaMain.py ${n} 1 &
sleep 1
python3 ./HotstuffReplicaMain.py ${n} 2 &
sleep 1
python3 ./HotstuffReplicaMain.py ${n} 3 &
sleep 1
python3 ./HotstuffReplicaMain.py ${n} 4 &
sleep 1
python3 ./ClientMain.py ${n} 1 512;


#for i in {1..32};
#do
#    echo ${i}
#    python3 ./ReplicaMain.py ${n} ${i} &
#    sleep 1
#done
#python3 ./ClientMain.py ${n} 1 2048;