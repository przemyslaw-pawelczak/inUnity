#!/bin/bash

# Set Repetitions
REP=1

echo "Run Evaluation CRC-Global"
cd crc_global_mini/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation CRC-Stack"
cd crc_stack_mini/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation AES-Global"
cd aes_global_mini/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation AES-Stack"
cd aes_stack_mini/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation FFT-Global"
cd fft_global_mini/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation FFT-Stack"
cd fft_stack_mini/
perf stat -r $REP -B python3 run.py
cd ..