#!/bin/bash

# Set Repetitions
REP=10

echo "Run Evaluation Input1"
cd input1/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation Input4"
cd input4/
perf stat -r $REP -B python3 run.py
cd ..