# Main controller for Task Dialog Manager
#
# Controls a set of modules, which handle sets of tasks. Tasks are as defined in the Task.py class,
# python Task.py		will create a sample task in the defined tasks directory
#
# To run:
#    python tdm.py				(python2 tdm.py on osx)
#
# To stop:
#    ctrl-c
#
# Author: jacky mallett (c) IIIM
# Version 2 appended and changed byt
#           : David Orn - david@iiim.is

import sched, time


# Root takes care of creating a root for the decision tree
# and maintains 
# Task was created by Jacie @ iiim.is and is a wrapper for
# json implimentation of tasks, effectively creating a struct
# for the tasks

import logging
# Setup for logger
logging.basicConfig(format='[%(name)s] | %(asctime)s | %(message)s', level=logging.DEBUG, 
                   filename='tdm.log')


from Modules.Task import *
from Modules.TaskHandler import *
from Modules.actions import *
import Modules.static as static
from Modules.InfoBag import *
from Modules.prerequisites import *


logger = logging.getLogger(__name__)


# Basic variables set for TDM
DictionaryLocation= "Modules" # Directory containing task definitions 
START_ROOT = "FIND-SOMETHING-TODO-1"


# DEBUG SWITCH
debugOn = 1
debugCounter = 0


# Main Loop
if __name__ == "__main__":
   
   # Create dictionary of tasks, questions, actions
   initDictionaries(DictionaryLocation)
   
   if debugOn == 1:
       # additional debugging settings
       InfoBag.Bag["personFound"] = True 
       InfoBag.Bag["talkingToPerson"] = True

   for key in InfoBag.Bag.keys():
       print(key + " " + str(InfoBag.Bag[key]))
   # Give name of starting module
   root_task = static.tasks["FIND-SOMETHING-TODO-1"]

   print(50*'*')
   print("Setup finished, starting up task query protocol") 
   print(50*'*')
   print(2*"\n")
   while True:
        # The main function starts at the beginning of the tree
        # and tries to run down it.

        # Start 
        mainHandler = TaskHandler(root_task)
        logger.info("Started root: "+mainHandler.task.name)
        # TODO push the outcome of the main task
        # to a log file
        mainTest, reason = mainHandler.run()
        logger.debug(mainHandler.task.name)
        logger.debug("Finished circle: " + str(mainTest) + " " + reason)
        if not mainTest: 
            None
        
        if debugCounter > 6:
            break
        debugCounter += 1
        
   #    # Read Message from psyclone
   #    # Update Module/Tasks as appropriate
   #    # Any other actions
   #    # Provide user interaction - kill switch/debug etc.
  
