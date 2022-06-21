# CMake toolchain file for Clang

set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CONFIG_DIR "${PROJECT_SOURCE_DIR}/config/cfg_stack_clang")

set(OUTPUT_SUFFIX ".elf" CACHE STRING "")
set(LINKER_SCRIPT "${CONFIG_DIR}/linkerscript.ld")
set(STARTUP_CODE "${CONFIG_DIR}/startup.c")

set(CMAKE_C_COMPILER    "clang")
#set(CMAKE_CXX_COMPILER  "clang")
set(CMAKE_AR            "llvm-ar")
set(CMAKE_LINKER        "ld.lld")
#set(CMAKE_LINKER        "arm-none-eabi-ld")
set(CMAKE_NM            "llvm-nm")
#set(CMAKE_OBJDUMP       "llvm-objdump")
set(CMAKE_OBJDUMP       "arm-none-eabi-objdump")
set(CMAKE_STRIP         "llvm-strip")
set(CMAKE_RANLIB        "llvm-ranlib")
set(CMAKE_SIZE          "llvm-size")

# General compiler flags
add_compile_options(
    -mthumb
    -mcpu=cortex-m4
    -march=armv7e-m+nofp
    -mfloat-abi=soft
    --target=thumbv7em-unknown-none-gnu
    -I/home/felix/Desktop/inUnity/code/config/cfg_stack_clang/lib/include
    )


# Toolchain include directories
 include_directories(
     )

# Device linker flags
#TODO Find a nice way to find the arm-gcc libraries, this is awful
add_link_options(
    -mcpu=cortex-m4
    -march=armv7e-m+nofp
    -mfloat-abi=soft
    --target=thumbv7em-unknown-none-eabi
    -nodefaultlibs

    # TODO: Fix!
    -L/home/felix/Desktop/inUnity/code/config/cfg_stack_clang/lib/gcc
    -L/home/felix/Desktop/inUnity/code/config/cfg_stack_clang/lib/libc

    -Wl,--Bstatic
    -Wl,-lc_nano
    -Wl,-lnosys
    -Wl,-lgcc
    )
