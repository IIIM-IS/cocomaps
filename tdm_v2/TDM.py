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
    def __init__(self, api=None):
        # Start by defining the loggers
        Logging.tdmLogging.setup_log()

        # This is for psyclone connection
        self.api = api
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

        # Set a variable that holds who it is talking to
        self.who_are_you = None
        # Define variable that holds the persons found in converstation, 
        # variable travels between tasks as a form of memeory
        self.persons = None

        # Define the specific functions, i.e. the actions that the
        # robot must act out
        self.Function_calls = ["ScheduleMeeting", 
                               "MakeCall", 
                               "GeneralQuestion"]

    def __del__(self):
        """
        Print out on screen that TDM exited correctly
        """
        print "TDM exited correctly"


    def run_task(self, task, parent=None):
        """
        Run an instance of a task, can call "subtasks" by calling new instance 
        of start_at
        """
        # Initializie the new task
        task._start_time = timer()

        # Handle specific tasks by forwarding them to their respective 
        # locations and returning their evaluations
        if task.name in self.Function_calls:
            # Get confirmation from user
            if(self.confirm(task.question_template[
                np.random.randint(
                    0, len(task.question_template)
                )
            ])):
               return eval("self.{}(task)".format(task.name))
            else:
                return False
        
        # Set task parent to value, if available, helps with debugging
        # and back tracking
        if parent:
            task.parent = parent.name


        # Currently unknown if all processable tasks will have questions
        if task.question_template:
            # Send a question to nuance output
            self.Nuance.write(
                task.question_template[
                   np.random.randint(0, len(task.question_template))
                ]
            )
            counter = 0
            failed = False
            asked = True
            for i in range(10):
                # Try to get user input 
                if not asked:
                    self.Nuance.write(
                        task.question_template[
                           np.random.randint(0, len(task.question_template))
                        ]
                    )
                
                prob, persons, ABORT = self.MEx.eval(self.Nuance.read(), 
                                                     task.keywords)
                self.logger.debug("Output : {} | {} | {}".format(prob, 
                                                                 persons, 
                                                                 ABORT))

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
                    if self.confirm("Continue with action: {}".format(
                        cont_obj
                    )):
                        self.persons = persons
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

                # If the loop reaches here then we need to ask the 
                # question that again, so that the user knows what the
                # input question is. Therefore we set this bool variable
                asked = False

                # Check if time has exceeded
                if (timer() - task.start_time)> task.max_time:
                    self.logger.info("Task max time exceeded")
                    failed = True
                    break
                    

                # If overall tries max at 10 then there is something wrong
                # and the program should abort current task
                if i == 9:
                    self.logger.info("Unable to get task input, maxing out \
                                    of overall tries")
                    failed = True
                    break

            if failed:
                return False


            # Assuming the task made it to here, it has been succsessfully
            # handled, return true
            return True


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
        Contrary of confirm, ask user if he wants to abort the action
        """
        self.Nuance.write(output_string)
        prob, _, ABORT = self.MEx.eval(self.Nuance.read(), ["accept", "deny"])
        if(prob[0] >= prob[1]) or ABORT:
            return False
        return True

    def find_person_in_sentance(self):
        """
        Get a person name, search the database for said name, if found
        return person object
        """
        

    def start_name(self, json_name, task=None):
        """
        Run an instance of the tdm starting from the named json file
        """
        new_task_instance = self.Tasks.Task[json_name]
        self.run_task(new_task_instance, task)
        


    def check_for_person(self):
        """
        Monitors if there is a person in the vicinity, if there is
        """
        # TODO Add this functionality
        # Start by querying who is in the conversation
        # Ask psyclone who's id has been found

        # I think it will be something like this
        #self.who_are_you.append(self.api.getVariable("PersonID"))
        
        return True

    def reset_TDM(self):
        """
        Between interaction a list of variables, and or parameters
        must be reset, changed or cleaned
        """
        self.who_are_you = None
        self.persons = None


    # # # # # # # # # # Function calls
"""
    def ScheduleMeeting(self, task):
        task.start_time = timer()
        self.logger.debug("Starting new task, ScheduleMeeting")
        meeting = 
        # Get who, multiple time
        if self.persons:
            for person in self.persons:
                self.Nuance.write("Want to meet with {}".format(person))
                if self.confirm("Accept this person to meeting"):
                    

        # Check if there are any other persons
        test_for_others = True
        while test_for_others:
            self.logger.debug("Asking for additional persons")
            self.Nuance.write("Would you like to add more persons to the \
                              meeting?")


        
        if(timer() - task.start_time) > task.max_time:
            self.logger.info("Schedule meeting timer maxed")
            return False
        return True
"""

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
