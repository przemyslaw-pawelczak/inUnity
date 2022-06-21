#!/bin/bash

# Set Repetitions
REP=10

cd build
echo "Run Evaluation CRC-Global"

perf stat -r $REP -B ../../icemu/bin/icemu \
  ./crc/crc-testcode.elf  \
  -c ../config/cfg_global_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT

echo "Run Evaluation AES-Global"

perf stat -r $REP -B ../../icemu/bin/icemu \
  ./randfolder/randfolder-testcode.elf  \
  -c ../config/cfg_global_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT

echo "Run Evaluation FFT-Global"

perf stat -r $REP -B ../../icemu/bin/icemu \
  ./fft/fft-testcode.elf  \
  -c ../config/cfg_global_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT

cd ..
