#!/bin/bash

../icemu/bin/icemu \
  ./example/example-testcode.elf  \
  -c ../icemu/example/cfg/cfg_armv7.json \
  #-p ./build/plugins/mock_putc_plugin.so \
  #-p ./build/plugins/inunit_plugin.so \
  #-a checkpoint-variable=CHECKPOINT \
  #-p ./build/plugins/display_instructions_plugin.so \
  #./arm-code/apps/inunit/inunit-wrapper.elf  \