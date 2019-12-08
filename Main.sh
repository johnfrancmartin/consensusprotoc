#!/usr/bin/env bash

killall python
killall python3
source ./venv/bin/activate;
python ./CreateBLS.py 2 4;
python ./ReplicaMain.py 4 1 &
python ./ReplicaMain.py 4 2 &
python ./ReplicaMain.py 4 3 &
python ./ReplicaMain.py 4 4;