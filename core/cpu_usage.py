#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import psutil as ps
import time # to sleep!

"""
Class that can measure CPU usage during the execution of the algorithm,
and report statistics about it at the end of it
 
Code inspired from here: https://stackoverflow.com/questions/2311301/reliably-monitor-current-cpu-usage
"""


class CpuPercent(threading.Thread):

    """
    Keep track of cpu usage.
    """
    def __init__(self):
        super(CpuPercent, self).__init__()
        self.cpuBuffer = []
        self.hasToMeasure = True

    """
    Defines the behaviour of this Thread, i.e.,
    the code to execute in this thread while it's alive.
    
    This Thread will measure the CPU usage and fill a buffer with the value every seconds.
    The buffer will be output when the algorithm has finished running, and the program is about to exit.
    """
    def run(self):

        while self.hasToMeasure:
            self.cpuBuffer.append(ps.cpu_percent(interval=1))
            time.sleep(1)

        print("CPU usage :\n")

        i = 0
        for usage in self.cpuBuffer:
            print("\tusage")
            if i == 5:
                print("\n")
                i = 0