import logging

# [LOGGING SETUP]
LOGGING_ENABLED = False
LOGGING_LEVEL = logging.CRITICAL

# [PARSER LOGGING SETUP]
LOG_SECTION_CONTENT = False
PARSER_LOG_LEVEL = logging.CRITICAL

# [DEBUG NAME]
test_name = 'program'

# [TESTING FILE CONFIGURATION]
file = 'source.ll'

# [TEST OUTPUT CONFIG]
save_test_results = True
save_llvmir_code = True
save_vm_state = True
save_dir = 'analysis_results'

# [TEST TO RUN]
run_continuous             = False
run_locate_memory_test     = True
run_evaluate_memory_test   = False
run_input_consistency_test = False
run_output_profiling       = False
run_profiling              = False

# [PROGRAM CONFIGURATION]
program_configuration = {
    'ir_function_prefix': '@', #llvm ir function name prefix
    'main_function_name': 'main',
    'before_restore_function_name': 'sceptic_before_restore',
    'after_restore_function_name': 'sceptic_after_restore',
    'before_checkpoint_function_name': 'sceptic_before_checkpoint',
    'after_checkpoint_function_name': 'sceptic_after_checkpoint',
}

# [REGISTER FILE CONFIGURATION]
register_file_configuration = {
    'use_physical_registers': False,
    'physical_registers_number': 10,
    'allocator_module_location': 'ScEpTIC.AST.register_allocation',
    'allocator_module_name': 'linear_scan',
    'allocator_function_name': 'allocate_registers', # nb: must take those arguments: functions, registers_number, reg_prefix, spill_prefix, spill_type
    'physical_registers_prefix': 'R',
    'spill_virtual_registers_prefix': '%spill_',
    'spill_virtual_registers_type': 'i32',
    'param_regs_count': 4 # number of registers used for passing parameters to functions (in arm/msp430 is 4)
}


# [EXECUTION DEPTH]
execution_depth = 3000

# [STOP ON FIRST ANOMALY]
stop_on_first_anomaly = False

# [SYSTEM CONFIGURATION]
system = 'custom'

# [MEMORY CONFIGURATION]
memory_configuration = {
    'sram': {
        'enabled': True,
        'stack': False,
        'heap': True,
        'gst': True,
        'gst_prefix': 'SGST',
        'gst_base_address': 0
    },
    'nvm': {
        'enabled': True,
        'stack': True,
        'heap': False,
        'gst': True,
        'gst_prefix': 'FGST',
        'gst_base_address': 0
    },
    'base_addresses': {
        'stack': 0,
        'heap': 0
    },
    'prefixes': {
        'stack': 'S',
        'heap': 'H'
    },
    'gst': {
        'default_ram': 'SRAM',
        'other_ram_section': '.NVM'
    },
    'address_dimension': 32
}


# [CHECKPOINT MECHANISM CONFIGURATION]

checkpoint_mechanism_configuration = {
    'checkpoint_placement': 'dynamic',
    'on_dynamic_voltage_alert': 'continue',
    'checkpoint_routine_name': 'checkpoint',
    'restore_routine_name': 'restore',
    'restore_register_file': True,
    'sram': {'restore_stack': True, 'restore_heap': True, 'restore_gst': True},
    'nvm': {'restore_stack': False, 'restore_heap': False, 'restore_gst': False},
    'environment': False
}


# [LOGGER SETUP FINALIZATION]
logging.basicConfig(format='[%(levelname)s - %(asctime)s] %(message)s', level=LOGGING_LEVEL, datefmt='%H:%M:%S')
logging.getLogger().disabled = not LOGGING_ENABLED

