#!/bin/bash

cmake -DCMAKE_TOOLCHAIN_FILE=./config/cfg_basic/toolchain.cmake "$@"

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $BASE_DIR

# Configure and make gcc versions
echo "Building ARM example code"
make