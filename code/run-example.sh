#!/bin/bash

../icemu/bin/icemu \
  ./example/example-testcode.elf  \
  -c ../icemu/example/cfg/cfg_armv7.json \
  -p ../icemu/build/plugins/unit_testing_plugin.so \
  -a checkpoint-variable=CHECKPOINT