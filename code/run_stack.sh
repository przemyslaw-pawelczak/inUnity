#!/bin/bash

# Set Repetitions
REP=1

cd build
echo "Run Evaluation CRC-Stack"

perf stat -r $REP -B ../../icemu/bin/icemu \
  ./crc/crc-testcode.elf  \
  -c ../config/cfg_stack_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT

echo "Run Evaluation AES-Stack"

perf stat -r $REP -B ../../icemu/bin/icemu \
  ./randfolder/randfolder-testcode.elf  \
  -c ../config/cfg_stack_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT

echo "Run Evaluation FFT-Stack"

perf stat -r $REP -B ../../icemu/bin/icemu \
  ./fft/fft-testcode.elf  \
  -c ../config/cfg_stack_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT

cd ..
