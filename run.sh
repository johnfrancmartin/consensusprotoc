#!/usr/bin/env bash
killall python
killall python3

source ./venv/bin/activate;
for i in {0..4}; do
    echo $i
    python3 ./replicannetwork.py $i &
    sleep 1
done
