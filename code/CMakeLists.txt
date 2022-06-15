cmake_minimum_required(VERSION 3.15)

message("Using toolchain file: ${CMAKE_TOOLCHAIN_FILE}")

project(test-code LANGUAGES C ASM)

add_subdirectory(example)
add_subdirectory(crc)
