#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import warnings

import psutil as ps

from core.algo.first_scenario import FirstScenario
# gets the number of physical AND logical cores
# available on the current machine
from core.algo.second_scenario import SecondScenario
from core.map.map_first_scenario import MapFirstScenario
from core.map.map_second_scenario import MapSecondScenario
from core.utils.cpu_usage import CpuPercent

nb__logical_cores = ps.cpu_count(True)


"""
A class that will run the whole program on a separate thread.
This is useful in order to run the simulation in background,
without blocking the GUI on the main Thread
"""


class Main(threading.Thread):

    def __init__(self, nbP, queue, args):
        super(Main, self).__init__()
        self.queue = queue
        self.args = args
        self.nbP = nbP

    '''
        Starts the project by outputting information about the processes only,
        without UI. 
    '''

    def noUI(self):
        print("Starting project with no UI!")
        cpuPercent = None

        if self.args.m:
            cpuPercent = CpuPercent(0)

        map = MapFirstScenario(self.nbP, False) if self.args.t == 0 else MapSecondScenario()
        algorithm = FirstScenario(map, self.nbP, None, False) if self.args.t == 0 else SecondScenario(map, self.nbP,
                                                                                                      None, False)

        if self.args.m:
            # finished setting up for simulation
            # start measurements
            cpuPercent.start()

        algorithm.startAlgo()

        if self.args.m:
            cpuPercent.stopMeasure()
            i = 1
            while i < 5:
                # here, we could have used a ThreadPool along
                # with an executor service to re-use this measurement thread
                # instead of re-creating one after each simulation.
                # however, the doc says that for the moment, due to the GLI,
                # multiprocessing API spawns subprocesses instead of threads, which
                # is less effective and heavier for the machine
                # see: https://docs.python.org/2/library/multiprocessing.html
                cpuPercent = CpuPercent(i)

                map = MapFirstScenario(self.nbP, True) if self.args.t == 0 else MapSecondScenario()
                algorithm = FirstScenario(map, self.nbP, None, True) if self.args.t == 0 else SecondScenario(map,
                                                                                                             self.nbP,
                                                                                                             None,
                                                                                                             False)

                cpuPercent.start()
                algorithm.startAlgo()
                cpuPercent.stopMeasure()

                print("Finished simulation number " + str(i))

                i += 1

            # need to join cpuPercent to let it finish writing in the file
            # the results of the last 5th simulation, or there will be a concurrency
            # problem for the res.json file
            cpuPercent.join()
            # returns the measurements for the 5 simulations
            cpuPercent.produce_report()

        self.queue.put("exit")

        return

    '''
        Starts the project by outputting information about the processes and by
        outputting through a UI. 
    '''

    def yesUI(self):
        print("Starting project with UI!")
        map = MapFirstScenario(self.nbP, True if self.args.m else False,
                               self.queue) if self.args.t == 0 else MapSecondScenario()
        algorithm = FirstScenario(map, self.nbP, self.queue,
                                  True if self.args.m else False) if self.args.t == 0 else SecondScenario(map,
                                                                                                          self.nbP,
                                                                                                          self.queue,
                                                                                                          True if self.args.m else False)
        algorithm.startAlgo()
        return

    """
    Overrides the default warnings.showwarning()
    function from the warnings package
    We need to override it because warning.warn() prints 
    the Python code of the warning to the user

    Here, we only return the msg of the warning and NOT the Python code

    see: https://stackoverflow.com/questions/2187269/python-print-only-the-message-on-warnings
    """

    def custom_formatwarning(self, msg, *a):
        # ignore everything except the message
        return str(msg) + '\n'

    def run(self):

        # more threads than CPU cores, raise a warning
        # because program may be slower than expected
        if self.nbP > nb__logical_cores:
            warnings.showwarning = self.custom_formatwarning
            warnings.warn("Provided number of threads is > to number of available cores\n"
                          "It may slow the execution of the program instead of accelerating it !!!\n"
                          "Number of available cores: " + str(nb__logical_cores), UserWarning)

        if self.args.m:
            self.noUI()
            exit(0)
        elif self.args.showUi == "true":
            self.yesUI()
            exit(0)
        else:
            self.noUI()
            exit(0)
