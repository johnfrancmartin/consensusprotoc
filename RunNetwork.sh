#!/usr/bin/env bash
killall python
killall python3

source ./venv/bin/activate;
n = 4
for i in {0..$n}; do
    echo $i
    python3 replicanetwork.py $i &
    sleep 1
done