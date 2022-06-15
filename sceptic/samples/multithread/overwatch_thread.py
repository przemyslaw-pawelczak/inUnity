import datetime
import threading
import time

class OverwatchThread(threading.Thread):
    """
    Thread for verifying ScEpTIC status
    """

    def __init__(self, sc):
        threading.Thread.__init__(self)
        self.sc = sc

    def run(self):
        latest_command = None

        while True:
            command = input('Command: ')

            if command == '\x1b[A' or command == '':
                command = latest_command

            if command == 'p':
                latest_command = 'p'
                space = ''

                for pc in self.sc.vm.state.register_file.pc._pc_tracking:
                    print('{}{} -> {}'.format(space, pc['function_name'], pc['instruction_number']))
                    space += ' '*4

                print('{}{}'.format(space, self.sc.vm.state.register_file.pc))

            elif command == 'c':
                latest_command = 'c'
                print('Global clock: {}'.format(self.sc.vm.state.global_clock))

            elif command == 's':
                latest_command = 's'
                print(self.sc.vm.get_visual_dump())

            elif command == 't':
                latest_command = 't'
                elapsed = time.time() - self.sc.start_time
                print('Elapsed time: {}\n'.format(datetime.timedelta(seconds=int(elapsed))))

            elif command == 'i':
                latest_command = 'i'
                for anomaly in self.sc.vm.state.anomalies:
                    print('{}\n'.format(anomaly))

            elif command == 'stop':
                latest_command = 'stop'
                print('Stopping...')

                while not self.sc.vm.state.force_stop:
                    self.sc.vm.stop_current_test()

                time.sleep(2)

            else:
                print('Available commands:')
                print('    p -> prints current program counter')
                print('    i -> prints current analysis results')
                print('    c -> prints current clock id')
                print('    s -> prints ScEpTIC state')
                print('    t -> prints the elapsed time')
                print('    stop -> stops current analysis')

                latest_command = None

            if not self.sc.isAlive():
                print('Test finished!')
                break
