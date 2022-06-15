#!/bin/bash

mkdir build
cd build

cmake -DCMAKE_TOOLCHAIN_FILE=../config/cfg_basic_clang/toolchain.cmake "$@"  ../

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $BASE_DIR

echo "Building ARM example code"
make

../../icemu/bin/icemu \
  ./evaluation_1/evaluation-1-testcode.elf  \
  -c ../config/cfg_basic_clang/cfg_armv7.json \
  -p ../../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT