#!/bin/bash

# Build Basic with globals on NVM
echo "Build Evaluation Basic-Global"
cd basic_global/
clang-6 -emit-llvm -S -g source.c
cd ..

# Build Basic with stack on NVM
echo "Build Evaluation Basic-Stack"
cd basic_stack/
clang-6 -emit-llvm -S -g source.c
cd ..

# Build Basic with heap on NVM
echo "Build Evaluation Basic-Stack"
cd basic_heap/
clang-6 -emit-llvm -S -g source.c
cd ..

# Build CRC with globals on NVM
echo "Build Evaluation CRC-Global"
cd crc_global/
clang-6 -emit-llvm -S -g main.c crc.c 
llvm-link-6 -S main.ll crc.ll -o source.ll
cd ..

# Build CRC with stack on NVM
echo "Build Evaluation CRC-Stack"
cd crc_stack/
clang-6 -emit-llvm -S -g main.c crc.c 
llvm-link-6 -S main.ll crc.ll -o source.ll
cd ..

# Build AES with globals on NVM
echo "Build Evaluation AES-Global"
cd aes_global/
clang-6 -emit-llvm -S -g main.c aes.c 
llvm-link-6 -S main.ll aes.ll -o source.ll
cd ..

# Build AES with stack on NVM
echo "Build Evaluation AES-Stack"
cd aes_stack/
clang-6 -emit-llvm -S -g main.c aes.c 
llvm-link-6 -S main.ll aes.ll -o source.ll
cd ..

# Build FFT with globals on NVM
echo "Build Evaluation FFT-Global"
cd fft_global/
clang-6 -emit-llvm -S -g main.c fftmisc.c fourierf.c
llvm-link-6 -S main.ll fftmisc.ll fourierf.ll -o source.ll
cd ..

# Build FFT with stack on NVM
echo "Build Evaluation FFT-Stack"
cd fft_stack/
clang-6 -emit-llvm -S -g main.c fftmisc.c fourierf.c
llvm-link-6 -S main.ll fftmisc.ll fourierf.ll -o source.ll
cd ..
