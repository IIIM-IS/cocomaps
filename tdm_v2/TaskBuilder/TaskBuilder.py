#!/usr/bin/python2.7
"""
24.01.18
Author
    david@iiim.is

Objective
    Tasks in the cocomaps project define the structure of actions that can
    be performed. Tasks incorporate information that is needed to move onto
    the next task, or send specific instructions to a source.
"""

import json
import os
import logging

class Task(object):
    """
    A wrapper around an actual json filename, using later
    defined specific implemmentation to load and store
    the set of tasks defined in tdm_v2/TaskBuilder/tasks/
    """
    def __init__(self, name, description, keywords, question_template, 
                 misc, fail_action, pass_action, max_time):
        """
        Initialize a task object; include adding dynamically addjusted
        variables
        """

        # Info from .json struct
        # TODO Add values that can help
        self.name = name
        self.description = description
        self.keywords = keywords
        self.question_template = question_template
        self.misc = misc
        self.fail_action = fail_action
        self.pass_action = pass_action
        self.max_time = max_time

        # Dynamically added values
        self._parent = None
        self._start_time = -1
        self._elapsed = 0

    @staticmethod
    def object_decoder(obj):
        """
        Object decoder for tasks
        """
        if "name" in obj:
            return Task(obj["name"], obj["description"], obj["keywords"],
                        obj["question_template"], obj["misc"], obj["fail_action"],
                        obj["pass_action"], obj["max_time"])
        return obj


class TaskBuilder(object):
    """
    Using an object stucture to store the json built tasks
    """
    def __init__(self, _type="run"):

        # For debugging purposes I can pass inn a specific logger (terminal)
        # if there isn't a logger then we can create the specific logger
        
        # Setup debug mode
        if _type=="run":
            self.debug = 0
            self.logger = logging.getLogger(__name__)
        elif _type=="debug":
            self.debug = 1
            fileh = logging.FileHandler('TaskBuilder_debug.log', 'a')
            formatter = logging.Formatter("%(asctime)s-%(funcName)s%(message)s")
            fileh.setFormatter(formatter)
            self.logger = logging.getLogger()  # root logger
            for hdlr in self.logger.handlers[:]:  # remove all old handlers
                self.logger.removeHandler(hdlr)
            self.logger.addHandler(fileh)
            self.logger.setLevel(logging.DEBUG)
        else:
            raise IOError("TaskBuilder needs to be set to 'debug' or 'run'")
    
        self.logger.info("Started Task builder")    

        self.Task = {}
        self.curr_loc = os.getcwd()


        # For debugging purposes
        # call comes either from debug, i.e. here
        # or from running i.e. tdm_v2 folder
        temp = self.curr_loc.split('/')
        if temp[-1] == "TaskBuilder":
            add_value = '/tasks/'
        elif temp[-1] == "tdm_v2":
            add_value = 'TaskBuilder/tasks/'
        else:
            raise WrongCallbackLocationError("Unable to build Task, wrong \
                                             location for function callback")
        self.task_file_location = self.curr_loc + add_value
        self.logger.debug("File location of .json \
                          files believed in {}".format(self.task_file_location))

        # Loading tasks into struct
        for task_file in os.listdir(self.task_file_location):
            file_type = os.path.splitext(task_file)[1]
            if file_type == ".json":
                long_file_name = self.task_file_location+task_file
                self.logger.debug("Loading file {}".format(long_file_name))
                with open(long_file_name, 'rb') as fptr:
                    txt = fptr.read()
                    tmp_task = json.loads(txt, object_hook=Task.object_decoder)
                    self.Task[tmp_task.name] = tmp_task
                    self.logger.info("Added task :{}".format(tmp_task.name))
        self.logger.info("Finished creating tasks")



# Error definitions specific to the object

class WrongCallbackLocationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class JsonFileError(Exception):
    def __init__(self, value):

        self.value = value

    def __str__(self):
        return repr(self.value)

# Debug main function, run if function is called directly
if __name__=="__main__":
    obj = TaskBuilder( _type="debug")
    print "Finished running main for Taskbuilder.py"
    print 2*'\n'
    print 50*"*"
    os.system("cat TaskBuilder_debug.log")
    print 50*"*"
