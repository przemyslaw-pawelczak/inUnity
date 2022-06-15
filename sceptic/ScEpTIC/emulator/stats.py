import time
import datetime

class ScEpTICStats:
    """
    Stats of ScEpTIC simulation
    """

    def __init__(self):
        self._initialize_stats()
        self.test_name = 'test'

    def reset(self):
        self._initialize_stats()

    def _initialize_stats(self):
        self.executed_instructions = 0
        self.executed_checkpoints = 0
        self.restored_checkpoints = 0
        self.executed_dumps = 0
        self.restored_dumps = 0

        self.anomalies = 0
        
        self.start_time = {'date': datetime.datetime.now().replace(microsecond=0), 'time': time.time()}

        self.stop_info = None

        self.forced_duration = 0

    def stop_at(self, pc, clock, is_anomaly = False):
        info  = ' Test stopped by user at clock: {}\n'.format(clock)
        info += ' Test stopped by user at program counter:\n{}\n'.format(pc)
        info += ' Stop reason: {}\n'.format('anomaly found.' if is_anomaly else 'user-forced.')
        
        self.stop_info = info

    def instruction_executed(self):
        self.executed_instructions += 1

    def checkpoint_executed(self):
        self.executed_checkpoints += 1
        self.executed_dumps += 1

    def checkpoint_restored(self):
        self.restored_checkpoints += 1

    def dump_restored(self):
        self.restored_dumps += 1

    def anomaly_found(self, count = 1):
        self.anomalies += count


    def __str__(self):
        retstr  = '[{}]\n'.format(self.test_name)
        retstr += ' Instruction executed: {}\n'.format(self.executed_instructions)
        retstr += ' Checkpoints executed: {}\n'.format(self.executed_checkpoints)
        retstr += ' Checkpoints restored (resets): {}\n'.format(self.restored_checkpoints)
        retstr += ' Dump executed: {}\n'.format(self.executed_dumps)
        retstr += ' Dump restored: {}\n'.format(self.restored_dumps)
        retstr += ' Anomalies found: {}\n\n'.format(self.anomalies)
        retstr += ' Simulation started at: {}\n'.format(self.start_time['date'])

        duration = datetime.timedelta(seconds=int(time.time() - self.start_time['time'])) if self.forced_duration == 0 else self.forced_duration

        retstr += ' Simulation duration: {}\n'.format(duration)
        
        try:
            instruction_speed = self.executed_instructions // int(time.time() - self.start_time['time'])

        except ZeroDivisionError:
            instruction_speed = 'NaN'

        if self.forced_duration > 0:
            instruction_speed = self.executed_instructions // self.forced_duration

        try:
            checkpoint_speed = round(self.executed_checkpoints / int(time.time() - self.start_time['time']), 2)

        except ZeroDivisionError:
            checkpoint_speed = 'NaN'

        retstr += ' Speed: {} instructions/s\n'.format(instruction_speed)
        retstr += '        {} checkpoints/s\n'.format(checkpoint_speed)

        if self.stop_info is not None:
            retstr += self.stop_info
        
        return retstr
