#!/usr/bin/env bash

killall python
killall python3
source ./venv/bin/activate;
pip list;
python3 ./CreateBLS.py 2 4;
python3 ./ReplicaMain.py 4 1 &
python3 ./ReplicaMain.py 4 2 &
python3 ./ReplicaMain.py 4 3 &
python3 ./ReplicaMain.py 4 4;