#! /usr/bin/env python
#################################################################################
#     File Name           :     TDM.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-28 14:44]
#     Last Modified       :     [2018-03-01 14:07]
#     Description         :     (T)ask (D)ialog (M)anager for the cocomaps project
#                               control the flow of task by requiering information
#                               asking for that relevant information and trying
#                               to move a task forward until user is happy with
#                               result. (Happy = Task Reached)
#     Version             :     4.0.1
#################################################################################

# Timing and other system imports
from timeit import default_timer as timer
import os, json
import time # For debugging reasons

# For logging reasosn
import logging
import tdm_logger

# Project specific imports
from Objects.TDM_objects import Objects
from Objects.TDM_objects import ActionStack
from Objects.TDM_objects import Word_Bag
from MEx.MEx import MEx

class TDM(object):
    """
    Task dialog manager object. Stores the current state of interaction and
    returns values that are required to achieve certain tasks.
    """
    def __init__(self):
        """
        Initialize all relevant information based on internal structure.
        Load all possible objects and load the MEx dictionary
        """
        # TODO add timing functionality to the system

        # Setup a default logging methodology.
        tdm_logger.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting TDM")

        # Create databases
        self.OBJ = Objects()
        self.MEx = MEx()
        self.Word_Bag = Word_Bag()

        # Create empty stack for actions
        self.Action_stack = ActionStack(self.MEx)

        # Dynamic variables for runtime
        self.current_state = "Empty"
        self.greeted = False
        self.current_task = None

    def run(self):
        self.logger.debug("Current status: {}".format(self.current_state))
        if self.Action_stack.getErrorCount() > 3:
            self.clean()
            return {"Fail":True, "Reason":"ToManyErrorCounts"}
        if self.current_state == "Information":
            # Check if the information missing from the action is in the 
            # word bag. If so move to action state. Else return question 
            # to get information for current action.
            enough_info, probability = self.Action_stack.info_check(self.Word_Bag)
            if enough_info:
                # If information is in the value set to 
                # action and start execution
                self.current_state = "Action"
                _dict = {}
                _dict["p"] = probability

                # Compute probability of keywords in sentence
                value = self.Action_stack.run_action(self.current_task, 
                                                   probability)
                if "Internal" in value.keys():
                    if value["Internal"] == "new_task":
                        self.logger.debug("Starting up new task: {}".format(value["name"]))
                        self.add_task(self.OBJ.new_object(
                            {"Type":"Tasks",
                             "Name":value["name"]}
                                                         ))
                        return {"Result":"NothingToDo"}
                return value
            else :
                # Run the action of aquiring more information
                return self.Action_stack.get_info(self.current_task)

        elif self.current_state == "Action":
            # POSSIBLE : Add connection to outside to look for confirmation
            # that task is complete.
            self.Action_stack.pop()
            if self.Action_stack.isEmpty():
                self.current_state = "Empty"
            else:
                self.logger.debug("Setting current state to information")
                self.current_state = "Information"
            return self.run()
        elif self.current_state == "Empty":
            self.logger.debug("Trying to reset empty queue")
            # Special case, the task list is empty, happens at beginning 
            # when everything is initialized and at reset intervals
            if not self.greeted:
                # Create greet action and put state machine in action format
                self.logger.debug("Adding Greet task to Task stack")
                self.add_task(self.OBJ.new_object({
                    "Type":"Tasks",
                    "Name":"Greet"
                }))
                self.greeted = True
                return self.run()

            else : 
                self.logger.debug("Adding Get_Objective to empty Task stack")
                self.add_task(self.OBJ.new_object({
                    "Type":"Tasks",
                "Name":"Get_Objective"
            }))
            return self.run()
        else :
            # If this is running something went wrong
            raise ValueError("TDM-run(else) line 62 - input of wrong type")


    def add_task(self, task):
        """
        Add a task to the current run. Take all actions in the task and 
        add to stack to be evalued consequitively.
        """
        # Check if action stack is empty. We can't start a new task 
        # if something is on the action task
        if self.Action_stack.isEmpty():
            self.Action_stack.resetErrorCount()
            self.current_task = task
            # Add action to action stack
            for action in task.actions:
                self.Action_stack.add(self.OBJ.new_object({
                    "Type":"Actions",
                    "Name":action
                }))
                # If a new task is created the system automatically 
                # sets the default input to information
                self.current_state = "Information"
        else : # What happens if the system tries to create a new task
                # while the action stack isn't empty
            return {"Fail":True, "Reason":"InternalError: Tried to create new task while action stack not empty"}
    
    def clean(self):
        """
        Empty both stacks. 
        """
        self.current_task = None
        self.Action_stack.clean()
    def add_words(self, input):
        """
        Top level for adding the input stream into the Word_Bag
        """
        self.Word_Bag.add(input)
                
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
# # # # # # # Functions for information, decorations  # # # # # # # # # #  
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
    def create_version(self):
        """
        Get information about the current iteration version, 
        what is active and what needs more work
        """
        current_folder = os.getcwd().split('/')[-1]
        tdm_version_file = "TDM_version.json"
        if current_folder != "TDM":
            tdm_version_file = "TDM/"+tdm_version_file
            
        with open(tdm_version_file, 'rb') as fid:
            data = fid.read()
            data = json.loads(data)
        self.data = data    
        self.version = data["Version"]

    def version_notes(self):
        """
        Print out the version notes for TDM
        """
        print 70*'*'
        print "\t\tVersion notes"
        print 70*'*'
        print "Author \t\t: {}".format(self.data["author"])
        print "Version no\t: {}".format(self.data["Version"])
        print "Release date\t: {}".format(self.data["Release"])
        print "Stable\t\t: {}".format(self.data["Stable"])
        print "Active modules"
        print "\tMEx"
        print "Available objects"
        for obj in self.data["objects"]:
            print "\t {}".format(obj)
        print "Author release notes"
        print "\t{}".format(self.data["Notes"])
        print 70*'*'
        print 70*'*'


if __name__=="__main__":
    obj = TDM()
    test_sentences = [
        "Move the other robot to location three",
        "Start up the generator",
        "Tell me a joke"
    ]

    data = obj.run()
    print "Initial data : {}".format(data)
    data2 = obj.run()
    print "Run 2 returns :{}".format(data2)
    for sent in test_sentences:
        obj.add_words(sent)
        for k in range(3):
            data = obj.run()
        print "data: {}".format(data)

