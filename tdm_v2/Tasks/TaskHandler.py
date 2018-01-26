#!/usr/bin/python2.7
"""
26.01.18
Author
    david@iiim.is

Objective
    Setup a reliable method of controlling and using the tasks that have already
    been built. 

Requirements:
    Controllable by creating a new task .json file

"""
import TaskBuilder
import actions_lib as do
import os
import logging
from timeit import default_timer as timer
import datetime
import numpy as np

class TaskHandler(object):
    """
    Class for handling and running tasks, the TashHandler creates and
    builds the system, here the objects are actually used and defined
    """
    def __init__(self, Nuance_instance, _type="run"):
        """
        Initialize new object with two possible types, one is run for main
        objective, not used, the other is to set _type to 'debug', then the
        debug output files are added
        """
        
        if _type == "run":
            self.debug = 0
            self.logger = logging.getLogger(__name__)
        elif _type == "debug":
            self.debug = 1
            fileh = logging.FileHandler("TaskHandler.debug", 'w')
            formatter = logging.Formatter("%(asctime)s-%(filename)s-%(funcName)s%(message)s")
            fileh.setFormatter(formatter)
            self.logger = logging.getLogger()
            for hdlr in self.logger.handlers[:]:  # remove all old handlers
                self.logger.removeHandler(hdlr)
            self.logger.addHandler(fileh)
            self.logger.setLevel(logging.DEBUG)
        else:
            raise IOError("Wrong input type (run/debug) in TaskHandler")
        self.Nuance = Nuance_instance
        
        self.logger.info("Started TaskBuilder")
        self.Tasks = TaskBuilder.TaskBuilder(_type, self.logger)



    def run_task(self, task, parent_name=None):
        """
        Create a new instance of the class object and work on that object 
        until pass/fail
        """
        new_task = task
        new_task.start_time = timer()

        

        # Randomly select one of the output questions to get action




        
        
            
    def run_json(self, json_id):
        """
        Starts running a specific json file, globally starts greet, also good
        for debugging
        """
        self.run_task(self.Tasks.Task[json_id])


# * * * * * * * * * DEBUGGING MAIN

if __name__ == "__main__":
    obj = TaskHandler("debug")
    print "Running specific json file: greet"
    obj.run_json('greet')

    print "Finished running debug on the TaskHandler"
    print 20*'*'
    print "Log file :"
    os.system("cat TaskHandler.debug")
    print 20*'*'

