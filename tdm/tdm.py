# Main controller for Task Dialog Manager
#
# Controls a set of modules, which handle sets of tasks. Tasks are as defined in the Task.py class,
# and modules are in Module.py. 
#
# python Task.py		will create a sample task in the defined tasks directory
#
# To run:
#    python tdm.py				(python2 tdm.py on osx)
#
# To stop:
#    ctrl-c
#
# Author: jacky mallett (c) IIIM

import sched, time
import os
import json
import sys
import static

# TODO: split out tasks into their modules

from Module import Module
from Task import Task

# Define globals 
static.init()

TASK_DIR = "tasks"            			# Directory containing task definitions ? Divide out into modules?
START_TASK = "FIND-SOMETHING-TODO-1"    # todo: how start?
modules = {}				   		    # Modules controlled by tdm

# Define Modules to be started/controlled

modules["YTTM"] = Module("YTTM")
modules["FC"]   = Module("FC")

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

       # Read in tasks from the directory and load into the tasks dictionary
       with open(TASK_DIR + "/" + filename, "r") as fptr:
           t =  fptr.read()
           task = json.loads(t,object_hook=Task.object_decoder)
           static.tasks[task.name] = task

   # Validate tasks, print out those that pass,  and exit if problems
   print "Loaded:"

   for task in static.tasks.values():
       if not checkTaskList(task.taskList):
          print task.name
          print "Unknown task in: %s" % ' '.join(map(str,task.taskList))
          sys.exit(0)
       print task.name
       print "\t%s" %' '.join(map(str,task.taskList))


   print "Starting: " + START_TASK
   task = static.tasks[START_TASK]

   # Start the modules 
   for module in modules.itervalues():
       module.start()
   
   # Set starting tasks for module(s)
   modules["YTTM"].newTask(static.tasks[START_TASK], True)

   # Main Loop for TDM
   while True:
       # Read Message from psyclone
       # Update Module/Tasks as appropriate
       # Any other actions
       # Provide user interaction - kill switch/debug etc.
       pass
      
