import copy

from .linear_scan import LinearScanRegisterAllocator

def allocate_registers(functions, registers_number, reg_prefix = 'R', spill_prefix = '%spill_', spill_type = 'i32'):
    """
    This functions performs the register allocation on the whole code (analysis, pre-processing, register allocation, and post-processing)
    """

    # perform register allocation on each function
    for function_name in functions:
        func = functions[function_name]

        # set the register allocator and run it
        func.register_allocator = LinearScanRegisterAllocator(func, registers_number, reg_prefix, spill_prefix, spill_type)
        func.register_allocator.run_register_allocation()

    # analyze register usage, to support call_post_processing
    compute_registers_usage(functions, registers_number)

    # do post-processing of functions calls. (insert register saving/restoring operations and set their tick_count)
    for function_name in functions:
        func = functions[function_name]
        func.register_allocator.do_call_post_processing()


def compute_registers_usage(functions, registers_number):
    """
    This function estimates the maximum register usage of each code's function and is used to
    estimate the actual number of operation performed for saving and restoring registers before
    a function call.
    Register allocation must be performed before running this function, so to have the number of registers used.

    A good partitioned register allocation will make registers from frequent functions call to not overlap, so to minimize
    the register saving operations before a function call.

    To estimate this scenario, is sufficient to find the number of registers used by each function (including the ones from the
    calls present in such function).

    The number of registers needed by a function is computed as:
        max(registers_used_by_internal_calls) + registers_used_by_function
        NB: recursive calls are ignored, since they will save the number of registers used by the current function.

    If this number is lower than the number of available registers, no saving is needed before the call.

    The overall number of register usage is calculated iteratively, since cycles can be possible (a calls b; b calls a;)
    If the number of needed registers exceed the number of available ones, a cycle-dependecy is found and thus all registers should be
    saved before such call.

    Initial setup: each function uses reg_count as max_reg_usage, calls is initialized with the functions called

    Iterate:
        find the max_reg_usage among the functions in calls
        set max_reg_usage = max_reg_usage of function calls + reg_count
        if max_reg_usage > max_available_registers -> max_reg_usage = max_available_registers

    until a fixed point is reached

    Once the max_reg_usage is found, call post-processing can be done (addition of registers saving/restoring routines)
    """

    function_data = {}
    old_function_data = {}

    # initialization step
    for function_name in functions:
        func = functions[function_name]
        function_data[function_name] = {'reg_count': func.reg_count, 'calls': func._calls, 'max_reg_usage': func.reg_count}

    # iterate until a fixed point is reached
    while function_data != old_function_data:
        old_function_data = copy.deepcopy(function_data)

        # update each value
        for name in function_data:
            f_data = function_data[name]

            # if the considered function exceed registers_number, skip (computation already done)
            if len(f_data['calls']) == 0 or f_data['max_reg_usage'] >= registers_number:
                continue

            # find max reg usage for called functions and compute current max_reg_usage
            calls = []

            for sub in f_data['calls']:
                calls.append(function_data[sub]['max_reg_usage'])

            max_reg_usage = max(calls) + f_data['reg_count']

            # limit max_reg_usage to registers_number
            f_data['max_reg_usage'] = min(max_reg_usage, registers_number)

    # update functions with final results.
    for function_name in functions:
        func = functions[function_name]
        func.max_reg_usage = function_data[function_name]['max_reg_usage']
