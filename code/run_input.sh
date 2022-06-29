#!/bin/bash

# Set Repetitions
REP=1000

cd build
echo "Run Evaluation CRC-Global"

perf stat -r $REP -B ../../icemu/bin/icemu \
  ./input1/input1-testcode.elf  \
  -c ../config/cfg_basic_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT

  perf stat -r $REP -B ../../icemu/bin/icemu \
    ./input4/input4-testcode.elf  \
    -c ../config/cfg_basic_clang/cfg_armv7.json \
    -p ../../icemu/build/plugins/unit_testing_plugin.so \
    -a checkpoint-variable=CHECKPOINT

cd ..
