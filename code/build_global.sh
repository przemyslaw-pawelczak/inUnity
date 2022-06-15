#!/bin/bash

rm -r build
mkdir build
cd build

cmake -DCMAKE_TOOLCHAIN_FILE=../config/cfg_global_clang/toolchain.cmake "$@"  ../

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $BASE_DIR

echo "Building Global on NVM Version"
make

cd ..