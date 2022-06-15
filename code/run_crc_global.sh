#!/bin/bash

cd build
echo "Executing CRC Global"

../../icemu/bin/icemu \
  ./crc/crc-testcode.elf  \
  -c ../config/cfg_global_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT

cd ..