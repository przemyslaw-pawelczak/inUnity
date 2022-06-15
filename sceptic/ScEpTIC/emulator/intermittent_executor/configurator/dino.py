"""
DINO

Checkpoint mechanism: static
SRAM: stack, heap, gst;
NVM: gst;
Checkpoint content: sram, registers, nvm (versioning of nvm variables)
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
    'checkpoint_placement': 'static',
    'restore_register_file': True,
    'sram': {'restore_stack': True, 'restore_heap': True, 'restore_gst': True},
    'nvm': {'restore_stack': False, 'restore_heap': False, 'restore_gst': True},
    'environment': False
}
