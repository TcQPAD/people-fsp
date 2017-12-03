#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import psutil as ps
import time  # to sleep!
import json

"""
Class that can measure CPU usage during the execution of the algorithm,
and report statistics about it at the end of it
 
Code inspired from here: https://stackoverflow.com/questions/2311301/reliably-monitor-current-cpu-usage
"""


class CpuPercent(threading.Thread):
    """
    Keep track of cpu usage.
    """

    def __init__(self, execution_nb=0):
        threading.Thread.__init__(self)
        self.cpuBuffer = []
        self.json_format = {}
        self.execution_nb = execution_nb
        self.responseTime = 0
        self.hasToMeasure = True

    """
    Defines the behaviour of this Thread, i.e.,
    the code to execute in this thread while it's alive.
    
    This Thread will measure the CPU usage and fill a buffer with the value every seconds.
    The buffer will be output when the algorithm has finished running, and the program is about to exit.
    """

    def run(self):

        start_time = time.time()

        while self.hasToMeasure:
            self.cpuBuffer.append(ps.cpu_percent(interval=0))
            time.sleep(0.1)

        print("\nCPU usage :\n")

        i = 0
        for usage in self.cpuBuffer:
            print("\t" + str(usage) + "%"),
            i += 1
            if i == 5:
                print("\n")
                i = 0

        # measure response time
        self.responseTime = time.time() - start_time
        print("\n\nResponse time:\t" + str(self.responseTime) + " seconds\n")

        #self.save_res_to_file()

    """
    Saves the results of the execution to a
    JSON file
    The "a" mode allows to append to a file
    """
    def save_res_to_file(self):
        self.json_format["run_" + str(self.execution_nb)] = {"cpu_usage": json.dumps(self.cpuBuffer),
                                                             "res_time": self.responseTime}
        with open("res.json", "a") as res_file:
            # first execution
            if self.execution_nb == 0:
                res_file.write("[\n")
            elif self.execution_nb != 0:
                res_file.write(",\n")
            res_file.write("\t")
            json.dump(self.json_format, res_file)

            # last execution
            if self.execution_nb == 4:
                res_file.write("\n]")

    """
    Stops the measurement by setting the boolean
    self.hasToMeasure to False
    """

    def stopMeasure(self):
        self.hasToMeasure = False

    """
    Reads the file with the save measurements values, and
    displays them nicely on the standard output
    """
    def produce_report(self):
        with open("res.json", "rb") as res_file:
            content = res_file.read()

        data = json.loads(content)

        mean_cpu_usage = 0
        mean_res_time = 0
        cpt_cu = 0
        cpt_rt = 0
        run_cpt = 0

        for x in data:
            list_us = [float(i) for i in x["run_" + str(run_cpt)]["cpu_usage"].strip('[]').split(',')]
            for y in list_us:
                mean_cpu_usage += y
                cpt_cu += 1

            mean_res_time += float(x["run_" + str(run_cpt)]["res_time"])
            cpt_rt += 1
            run_cpt += 1

        print("\n\n\tMean CPU Usage of all 5 simulations:\t" + str(mean_cpu_usage/cpt_cu) + "%")
        print("\n\n\tMean Response Time of all 5 simulations:\t" + str(mean_res_time/cpt_rt) + "%\n")
