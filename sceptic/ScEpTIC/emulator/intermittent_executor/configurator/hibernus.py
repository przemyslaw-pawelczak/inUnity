"""
Hibernus

Checkpoint mechanism: dynamic
On Power Interrupt: stop
SRAM: stack, heap, gst;
NVM: gst;
Checkpoint content: sram, registers
"""

memory_configuration = {
    'sram': {
        'enabled': True,
        'stack': True,
        'heap': True,
        'gst': True
    },
    'nvm': {
        'enabled': True,
        'stack': False,
        'heap': False,
        'gst': True,
    }
}

checkpoint_mechanism_configuration = {
    'checkpoint_placement': 'dynamic',
    'on_dynamic_voltage_alert': 'stop',
    'restore_register_file': True,
    'sram': {'restore_stack': True, 'restore_heap': True, 'restore_gst': True},
    'nvm': {'restore_stack': False, 'restore_heap': False, 'restore_gst': False},
    'environment': False
}
