#!/bin/bash

# Build Input1
echo "Build Evaluation Input1"
cd input1/
clang-6 -emit-llvm -S -g source.c
cd ..

# Build Input4
echo "Build Evaluation Input2"
cd input4/
clang-6 -emit-llvm -S -g source.c
cd ..