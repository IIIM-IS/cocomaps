#!/usr/bin/python2.7
"""
Author
    david@iiim.is

About 
    Task Dialog(ue) Manager (TDM) for CoCoMaps project, a collaborative project
    with CMLabs and IIIM. The manager controls high level (course granular 
    timing) decision as well as giving instructions to the robot. 
"""
# Standard modules
import os
import time
from timeit import default_timer as timer
import numpy as np

# Custom modules
from MEx import MEx
from Tasks import TaskBuilder
from YTTM_connector import YTTM_talk
from Nuance import Nuance

# # # # # # DEBUG : CLEAN LOGGING FOLDER
os.system("find Logging/ -name *.log -exec rm {} \;")

# # # # # # DEBUG : END OF DEBUG

# Setup the logging module for getting, setting and storing information
import logging
import Logging.tdmLogging


class TDM(object):
    """
    The main task dialog object used to connect and interface with 
    pysclone
    """
    def __init__(self):
        # Start by defining the loggers
        Logging.tdmLogging.setup_log()

        self.logger = logging.getLogger(__name__)
        self.logger.debug("Debug msg")
        self.logger.info("Info msg")
        self.logger.warning("Warn msg")  

        # Create TDM specific objects, the tasks built from .json files
        # and the Meaning extractor (MEx).
        self.MEx    = MEx.MEx()
        self.YTTM   = YTTM_talk.YTTM_talk()
        self.Nuance = Nuance.Nuance()
        self.Tasks  = TaskBuilder.TaskBuilder()


    def __del__(self):
        """
        Deconstructor for TDM object to measure if object exists correctly
        """
        print "TDM exited correctly"


    def run_task(self, task, parent=None):
        """
        Run an instance of a task, can call "subtasks" by calling new instance 
        of start_at
        """
        # Initializie the new task
        task._start_time = timer()

        # Currently unknown if all processable tasks will have questions
        if task.question_template:
            # Send a question to nuance output
            self.Nuance.write(
                task.question_template[
                   np.random.randint(0, len(task.question_template))
                ]
            )
            counter = 0
            asked = True
            while True:
                # Wait for response
                
                if not asked:
                    self.Nuance.write(
                        task.question_template[
                           np.random.randint(0, len(task.question_template))
                        ]
                    )
                
                prob, persons, ABORT = self.MEx.eval(self.Nuance.read(), task.keywords)
                self.logger.debug("Output : {} | {} | {}".format(prob, persons, ABORT))

                if ABORT:
                    if not self.confirm("Abort action"):
                            # NOTE : This might be the worst idea in the history of 
                            # mankind with respect to security...
                            eval(task.fail_action)
                            self.logger.info("User aborted action")
                            break

                if np.amax(prob) > 0:
                    # Most probable next objective is 
                    print 
                    cont_obj = task.keywords[prob.argmax(axis=0)]
                    if self.confirm("Continue with action: {}".format(cont_obj)):
                        self.logger.info("User accepted action to continue: \
                                         {}".format(cont_obj))
                        break
                    # move onto the next question, and or task

                counter += 1

                if task.misc and "Tries" in task.misc.keys():
                    if counter > task.misc["Tries"]:
                        self.logger.info("Stopped asking, maxed number of \
                                         tries")
                        break
                asked = False


    def confirm(self, output_string):
        """
        Ask user to confirm the next output, input
        """
        self.Nuance.write(output_string)
        prob, _, ABORT = self.MEx.eval(self.Nuance.read(), ["accept", "deny"])
        if(prob[0] >= prob[1]) or ABORT:
            return True
        return False

    
    def deny(self, output_string):
        """
        Appothise of confirm, ask user if he wants to abort the action
        """
        self.Nuance.write(output_string)
        prob, _, ABORT = self.MEx.eval(self.Nuance.read(), ["accept", "deny"])
        if(prob[0] >= prob[1]) or ABORT:
            return False
        return True



    def start_at(self, json_name):
        """
        Run an instance of the tdm starting from the named json file
        """
        new_task_instance = self.Tasks.Task[json_name]
        self.run_task(new_task_instance)
        


    def check_for_person(self):
        """
        Monitors if there is a person in the vicinity, if there is
        """
        # TODO Add this functionality
        return True


# Psyclone cranc definition


# Debug function
if __name__ == "__main__":
    obj = TDM()
    # Test nuance output, send line for interpretation
    obj.start_at("get_objective")
    time.sleep(1)
    print "Debugging TDM finished"
    print 10*'*'
    print "Debug log output: "
    print 10*'*'
    os.system("cat Logging/*.log")
