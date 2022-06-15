import logging

from ScEpTIC.AST.builtins.builtin import Builtin
from ScEpTIC.emulator.io.output import OutputManager
from ScEpTIC.emulator.io.input import InputManager

# [LOGGING SETUP]
LOGGING_ENABLED = False
LOGGING_LEVEL = logging.CRITICAL
#LOGGING_LEVEL = logging.WARNING
#LOGGING_LEVEL = logging.INFO
#LOGGING_LEVEL = logging.DEBUG

# [PARSER LOGGING SETUP]
LOG_SECTION_CONTENT = False
PARSER_LOG_LEVEL = logging.CRITICAL

# [DEBUG NAME]
test_name = 'program'

# [TESTING FILE CONFIGURATION]
file = 'samples/base.ll'

# [TEST OUTPUT CONFIG]
save_test_results = True
save_llvmir_code = True
save_vm_state = True
save_dir = 'analysis_results'

# [TEST TO RUN]
run_continuous             = True
run_locate_memory_test     = True
run_evaluate_memory_test   = True
run_input_consistency_test = True
run_output_profiling       = True
run_profiling              = True

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
    'use_physical_registers': True,
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
# NB: ignored if checkpoint mechanism is static
execution_depth = 10

# [STOP ON FIRST ANOMALY]
# If set to True, if ScEpTIC finds a real anomaly, it stops
stop_on_first_anomaly = True

# [SYSTEM CONFIGURATION]
system = 'custom'
"""
Available systems: DINO, Hibernus, Mementos, Quickrecall, Ratchet, Custom
To add a system, add a .py file named with the system name you want to support in ScEpTIC/emulator/configurator/.
Use other system files as template.

Custom considers the user-defined settings for memory configuration and checkpoint mechanisms.
Addresses, prefixes and dimensions are never overwritten by pre-defined systems configurations.
The following configurations will be overwritten, if the system is different from 'custom':
    - memory_configuration['sram']['enabled']
    - memory_configuration['sram']['stack']
    - memory_configuration['sram']['heap']
    - memory_configuration['sram']['gst']

    - memory_configuration['nvm']['enabled']
    - memory_configuration['nvm']['stack']
    - memory_configuration['nvm']['heap']
    - memory_configuration['nvm']['gst']


    - checkpoint_mechanism_configuration['checkpoint_placement']

    - checkpoint_mechanism_configuration['on_dynamic_voltage_alert']

    - checkpoint_mechanism_configuration['restore_register_file']

    - checkpoint_mechanism_configuration['sram']['restore_stack']
    - checkpoint_mechanism_configuration['sram']['restore_heap']
    - checkpoint_mechanism_configuration['sram']['restore_gst']
    
    - checkpoint_mechanism_configuration['nvm']['restore_stack']
    - checkpoint_mechanism_configuration['nvm']['restore_heap']
    - checkpoint_mechanism_configuration['nvm']['restore_gst']
"""

# [MEMORY CONFIGURATION]
memory_configuration = {
    'sram': {
        'enabled': True,
        'stack': True,
        'heap': True,
        'gst': True,
        'gst_prefix': 'SGST',
        'gst_base_address': 0
    },
    'nvm': {
        'enabled': True,
        'stack': False,
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
        'default_ram': 'SRAM', # SRAM or NVM
        'other_ram_section': '.NVM'
    },
    'address_dimension': 32 # bit
}


# [CHECKPOINT MECHANISM CONFIGURATION]
"""
NB: if the checkpoint mechanism creates incremental checkpoints of nvm, it restores the whole nvm.
This configuration doesn't need to know the granularity of the checkpoint mechanism, it just needs to know
if something is restored (even partially).
checkpoint_placement can be static or dynamic. If it is set to static, checkpoints must be already present
inside the provided code. In such case, the user must provide the names of the checkpoint and restore routines.
on_dynamic_voltage_alert is considered only if checkpoint_placement is set to dynamic. it can be set on continue or stop.
if is set to stop, after a power interrupt the simulator will save a checkpoint and stop the execution (forces the execution_depth to 0).
if is set to continue, the simulator will save a checkpoint and continue the execution for #execution_dept operations (dynamic) or until another
checkpoint is reached (static).
"""
checkpoint_mechanism_configuration = {
    'checkpoint_placement': 'dynamic',
    'on_dynamic_voltage_alert': 'continue',
    'checkpoint_routine_name': 'checkpoint', # required if checkpoint_placement is static
    'restore_routine_name': 'restore',       # required if checkpoint_placement is static
    'restore_register_file': True,
    'sram': {'restore_stack': True, 'restore_heap': True, 'restore_gst': True},
    'nvm': {'restore_stack': False, 'restore_heap': False, 'restore_gst': False},
    'environment': False,
}


# [LOGGER SETUP FINALIZATION]
logging.basicConfig(format='[%(levelname)s - %(asctime)s] %(message)s', level=LOGGING_LEVEL, datefmt='%H:%M:%S')
logging.getLogger().disabled = not LOGGING_ENABLED


# [USER-DEFINED BUILTINS]

class Test(Builtin):
    
    tick_count = 2000
    
    def get_val(self):
        for i in self.args:
            print(i)

        print("OK")
        return self.args[3]

Prova.define_builtin('test_builtin', 'double, i32, i32, i32', 'i32')

# [USER-DEFINED OUTPUTS]
# 
# For output analysis, set the default idempotency model used for each output function
OutputManager.default_idempotent = True
OutputManager.create_output('test', 'output_1', 'i32')
OutputManager.create_output('test2', 'output_2', 'i32')

# For output analysis, set the idempotency model for a given output
OutputManager.set_idempotency('test', OutputManager.NON_IDEMPOTENT)

# [USER-DEFINED INPUTS]
InputManager.create_input('PIR', 'pir_input', 'i32')
InputManager.set_input_value('PIR', '10000000')
InputManager.set_consistency_model('PIR', InputManager.LONG_TERM)
