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
import os
import json
import sys
import Modules.static as static


# Root takes care of creating a root for the decision tree
# and maintains 
# Task was created by Jacie @ iiim.is and is a wrapper for
# json implimentation of tasks, effectively creating a struct
# for the tasks
from Modules.Task import Task as Task

# Import Psyclone list reader
#from Psy2Py import PsycloneList as Psy2Py


TASK_DIR = "Modules/tasks" # Directory containing task definitions 
START_ROOT = "FIND-SOMETHING-TODO-1"
root_ = []
# Initialize the 
static.init() 

# Validation - check that the task list for a task, represents tasks that 
# we know about
def checkTaskList(tasklist):
    for t in tasklist:
        if t not in static.tasks:
           return False
        else:
           return True
    return True

# Main Loop
if __name__ == "__main__":
   for filename in os.listdir(TASK_DIR):
       print(TASK_DIR + "/" + filename)
     
       # Read in tasks from the directory and load into the tasks dictionary
       with open(TASK_DIR + "/" + filename, "r") as fptr:
           t =  fptr.read()
           task = json.loads(t,object_hook=Task.object_decoder)
           static.tasks[task.name] = task
           if task.name == START_ROOT:
               root_ = Root(task)
   # Validate tasks, print out those that pass,  and exit if problems
   root_.setStaticTasks(static.tasks)
   print "Finished loading tasks:"
   for task in static.tasks.values():
       if not checkTaskList(task.taskList):
          print "Unknown task in: %s" % ' '.join(map(str,task.taskList))
          sys.exit(0)
       print(task.name)
   print(2*"\n")
   print(50*'*')
   print("Setup finished, starting up query tree protocol") 
   print(50*'*')
   print(2*"\n")
   # Create a Psyclone reader
   psyread = Psy2Py()
   psyread.start()
   # Start up root
   # root_.run() 
   bugCount = 1
   while True:
       time.sleep(1)
       root_.printTasks()
   #    # Read Message from psyclone
   #    # Update Module/Tasks as appropriate
   #    # Any other actions
   #    # Provide user interaction - kill switch/debug etc.
   #    pass
      
