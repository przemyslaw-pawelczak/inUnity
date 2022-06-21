#!/bin/bash

# Set Repetitions
REP=30

echo "Run Evaluation CRC-Global"
cd crc_global/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation CRC-Stack"
cd crc_stack/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation AES-Global"
cd aes_global/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation AES-Stack"
cd aes_stack/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation FFT-Global"
cd fft_global/
perf stat -r $REP -B python3 run.py
cd ..

echo "Run Evaluation FFT-Stack"
cd fft_stack/
perf stat -r $REP -B python3 run.py
cd ..
