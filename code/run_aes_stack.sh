#!/bin/bash

cd build
echo "Executing AES Stack"

../../icemu/bin/icemu \
  ./randfolder/randfolder-testcode.elf  \
  -c ../config/cfg_stack_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT

cd ..