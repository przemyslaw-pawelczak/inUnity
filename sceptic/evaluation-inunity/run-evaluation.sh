#!/bin/bash

# Set Repetitions
REP=1

echo "Run Evaluation Basic-Global"
cd basic_global/
perf stat -r REP -B python3 run.py
cd ..

echo "Run Evaluation Basic-Stack"
cd basic_stack/
perf stat -r REP -B python3 run.py
cd ..

echo "Run Evaluation Basic-Heap"
cd basic_heap/
perf stat -r REP -B python3 run.py
cd ..

echo "Run Evaluation CRC-Global"
cd crc_global/
perf stat -r REP -B python3 run.py
cd ..

echo "Run Evaluation CRC-Stack"
cd crc_stack/
perf stat -r REP -B python3 run.py
cd ..

echo "Run Evaluation AES-Global"
cd aes_global/
perf stat -r REP -B python3 run.py
cd ..

echo "Run Evaluation AES-Stack"
cd aes_stack/
perf stat -r REP -B python3 run.py
cd ..