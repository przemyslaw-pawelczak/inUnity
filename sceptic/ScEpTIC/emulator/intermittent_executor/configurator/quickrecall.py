"""
QuickRecall

Checkpoint mechanism: dynamic
On Power Interrupt: stop
SRAM: none;
NVM: stack, heap, gst;
Checkpoint content: registers (no problem since it stops the execution on interrupt)
"""

memory_configuration = {
    'sram': {
        'enabled': False,
        'stack': False,
        'heap': False,
        'gst': False
    },
    'nvm': {
        'enabled': True,
        'stack': True,
        'heap': True,
        'gst': True,
    }
}

checkpoint_mechanism_configuration = {
    'checkpoint_placement': 'dynamic',
    'on_dynamic_voltage_alert': 'stop',
    'restore_register_file': True,
    'sram': {'restore_stack': False, 'restore_heap': False, 'restore_gst': False},
    'nvm': {'restore_stack': False, 'restore_heap': False, 'restore_gst': False},
    'environment': False
}
