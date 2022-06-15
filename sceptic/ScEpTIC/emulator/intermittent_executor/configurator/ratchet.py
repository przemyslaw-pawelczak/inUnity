"""
Ratchet

Checkpoint mechanism: static
SRAM: none;
NVM: stack, heap, gst;
Checkpoint content: registers (checkpoints before WAR hazards, so re-execution is not a problem by design)
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
    'checkpoint_placement': 'static',
    'restore_register_file': True,
    'sram': {'restore_stack': False, 'restore_heap': False, 'restore_gst': False},
    'nvm': {'restore_stack': False, 'restore_heap': False, 'restore_gst': False},
    'environment': False
}
