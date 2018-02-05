#!/usr/bin/python2.7
"""
02.01.18
Author
    david@iiim.is

About 
    Task Dialog(ue) Manager (TDM) for CoCoMaps project, a collaborative project
    with CMLabs and IIIM. The manager controls high level (course granular 
    timing) decision as well as giving instructions to the robot. 
"""
__author__="david"
# General input values
import os
from timeit import default_timer as timer
import time
import numpy as np

# Specifically regarding logging
import tdm_logger 
import logging
# Objective specific imports
from MEx import MEx
from Nuance import Nuance
from YTTM import YTTM
from MEx.Types.Actions.action_lib import Action_Call


class TDM(object):
    """
    A class object, called from the cranc function and used to
    control the steams, dialogue and action
    """
    def __init__(self):
        # TDM starts up logging preferences
        tdm_logger.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Started TDM")


        self.MEx = MEx.MEx()
        self.YTTM = YTTM.YTTM_talk()
        self.NUANCE = Nuance.Nuance()

        # The action library takes in str value refering to which action to 
        # perform. There is an open amount of calls (i.e. *args) so all other 
        # information can be passed. 
        # Pass additional values in as a packed dict


    def get_input_request(self):
        obj = self.MEx.Types["Tasks"]["get_objective"]
        print obj.description


    def initialize(self):
        """
        The initialization process does the foGllowing 
            Once a person has been ackn. drive to the person
            and greet it, then ask for a task to perform.
        """
        self.logger.debug("Starting initialization")
        self.logger.info("Initialization of system starting")

        greet_task = self.MEx.Types["Tasks"]["greet"]
        self.task_manager(greet_task)

        time.sleep(1)
        self.NUANCE.write("Exiting mode")

    def task_manager(self, task):
        """
        Task Manager: Key function in class. A set of logical rules to 
        follow when executing a task. The json file decides how the 
        task is run and the action field in the json file is how the
        task is run (i.e. using keywords to run the sys)
        """
        self.logger.debug("Running task manager on {}".format(task.name))
        n = len(task.action)

        break_reason = None
        for idx, action in enumerate(task.action):
            # GoToGetObjective is a short circuit that breaks the current
            # flow and starts a new task setup
            if action != "new_task":
                self.logger.info("Running task {}, action {}".format(
                                                                    task.name,
                                                                    action))

                self.logger.debug("Running action {}".format(action))
                ans_case, reason = Action_Call(action, 
                                                        {"Task":task,
                                                         "NUANCE":self.NUANCE,
                                                         "MEx":self.MEx,
                                                         "YTTM":self.YTTM})
                # _dict is a return dict so, we can build a set of contingencies 
                # either in Actions or here to encounter what to do. 
                self.logger.debug("Action call : {}, {}, {}".format(
                                                    action,
                                                    ans_case,
                                                    reason
                ))
                if ans_case == False and reason == "rejected":
                    self.logger.debug("Rejected hypothesis ")
                    break


            elif action=="new_task" and reason != "rejected":
                break_reason = "new_task"
                break 


        if break_reason == "new_task":
            self.logger.debug("Starting new task from {} to {}".format(
                                                            task.name,
                                                            task.pass_action
                                                            ))
            ans_case, task = Action_Call("new_task", {"Task":task, 
                                                "YTTM":self.YTTM,
                                                "NUANCE":self.NUANCE,
                                                "MEx":self.MEx})
            if ans_case :
                self.logger.info("Starting new task : {}".format(task.name))
                self.task_manager(task)
            else:
                self.NUANCE.write("Something went wrong. Restarting process")
                restart_task = self.MEx.Types["Tasks"]["get_objective"]
                self.task_manager(restart_task)

        
        # Finished process, wait for a short time. Then ask user for a new 
        # input. 
        # I see no reason for the TDM not to just stop. Then psyclone 
        # can run it up again if so required.

        # Technically, when we reach this point we have a good exit from TDM




        
# Main is used as a debugging function
if __name__ == "__main__":
    obj = TDM()

    obj.initialize()
    
