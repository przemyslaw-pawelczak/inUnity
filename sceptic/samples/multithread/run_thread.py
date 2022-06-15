import datetime
import threading
import time
import sys

from overwatch_thread import OverwatchThread

import config
import ScEpTIC

sc = ScEpTIC.init(config)

class ScEpTICThread(threading.Thread):
    """
    Thread executing ScEpTIC analysis
    """

    def __init__(self, sc):
        threading.Thread.__init__(self)
        self.sc = sc

    def run(self):
        start_time = time.time()

        self.sc.run_tests()

        elapsed = time.time() - start_time

        print('Test done! Elapsed seconds: {}s ({})\n'.format(elapsed, datetime.timedelta(seconds=int(elapsed))))

sceptic_thread = ScEpTICThread(sc)
overwatch_thread = OverwatchThread(sceptic_thread)

sceptic_thread.start()
overwatch_thread.start()
