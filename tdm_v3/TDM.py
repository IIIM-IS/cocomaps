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
import json

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
        
        with open("TDM_version.json", 'rb') as fid:
            data = fid.read()
            data = json.loads(data)
        self.data = data    
        self.version = data["Version"]

    def get_input_request(self):
        obj = self.MEx.Types["Tasks"]["get_objective"]
        print obj.description

    def version_notes(self):
        print 10*'*'
        print "\t\tVersion notes"
        print 10*'*'
        print "Author \t:{}".format(self.data["author"])
        print "Version no\t: {}".format(self.data["Version"])
        print "Release date\t: {}".format(self.data["Release"])
        print "Stable\t\t: {}".format(self.data["Stable"])
        print "Active modules"
        print "\tMEx\t: {}".format(self.data["MEx"])
        print "\tYTTM\t: {}".format(self.data["YTTM"])
        print "\tNuance\t: {}".format(self.data["Nuance"])
        print "\tPsyclone\t: {}".format(self.data["Psyclone"])
        print "Available objects"
        print "\t {}".format(self.data["objects"])
        print "Author release notes"
        print "\t{}".format(self.data["Notes"])
        print 10*'*'
        print 10*'*'

    def initialize(self):
        """
        The initialization process does the foGllowing 
            Once a person has been ackn. drive to the person
            and greet it, then ask for a task to perform.
        """
        self.logger.debug("Starting initialization")
        self.logger.info("Initialization of system starting, {}".format(
            self.version
        ))

        greet_task = self.MEx.Types["Tasks"]["greet"]
        self.task_manager(greet_task)

        time.sleep(1)
        self.logger.debug("Exiting correctly")
        self.logger.info("Exiting correctly")
        self.NUANCE.write("Exiting correctly")

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
            # new_taskis a short circuit that breaks the current
            # flow and starts a new task 
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
                # Checking if the action returend false, and if it was
                # because of returning rejected (i.e. getting thrown out
                # by a question, want to continue == No)
                if ans_case == False and reason == "rejected":
                    self.logger.debug("Rejected hypothesis ")
                    break

            # Check if the current action name is 'new_task', and ensure that
            # the reason for return is not rejected, then start new task
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
                # task_manager function actually starts the new task
                self.task_manager(task)
            else:
                # A reset switch, something went wrong and therefore we want 
                # to start anew with the question what can robot do
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

    obj.version_notes()
    
