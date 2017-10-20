# Task definition for CoCoMaps project. 
#
# python Task.py   will create a sample task in the TASK_DIR directory.
#
# todo:  backup any existing tasks in the directory when invoked directly
#
# Author: jacky mallett (c) IIIM

import json
import os, sys
import static as static


TASK_DIR = "tasks"
class Task():
    def __init__(self, name, canBeActivated, prerequisites,functionCalls,
                 failureAction, timeOutAction, maxDuration, whatAmIDoing,
                 isActive, taskList):
        self.name             = name
        self.canBeActivated   = canBeActivated
        self.prerequisites    = prerequisites
        self.functionCalls    = functionCalls
        self.failureAction    = failureAction
        self.timeOutAction    = timeOutAction
        self.maxDuration      = maxDuration
        self.whatAmIDoing     = whatAmIDoing
        self.isActive         = isActive
        self.taskList         = taskList



    # Each element in the Task must be defined here for saving and loading to work
    @staticmethod
    def object_decoder(obj):
        if '__type__' in obj and obj['__type__'] == 'Task':
             return Task(obj['name'],           obj['canBeActivated'],
                         obj['prerequisites'],  obj['functionCalls'], 
                         obj['failureAction'],  obj['timeOutAction'],    
                         obj['maxDuration'],    obj['whatAmIDoing'],
                         obj['isActive'],       obj['taskList'])
        return obj



# If invoked directly, create a sample task and put it in the main directory

if __name__ == "__main__":
   o = json.loads('{"__type__":"Task", \
                    "name"            :"FIND-SOMETHING-TODO-1", \
                    "canBeActivated"  :"False", \
                    "prerequisites"   :[],  \
                    "functionCalls"   :"", \
                    "failureAction"   :"SEARCH-TASK-FAILED", \
                    "timeOutAction"   :"SLEEP", \
                    "maxDuration"     :"300000", \
                    "whatAmIDoing"    :"Lost in Space", \
                    "isActive"        :"False", \
                    "taskList"        :["LookAround", "AskForInput"]}',
                    object_hook=Task.object_decoder)
   print o.taskList[0]

   print "Creating task:"
   with open(TASK_DIR + "/" + o.name, "w") as fptr:
       out = json.dumps(o.__dict__,indent=4)
       fptr.write(out[0] + "\"__type__\":\"Task\"," + out[1:])
       print "\t" + o.name

def checkTaskList(tasklist):
    for t in tasklist:
        if t not in static.tasks:
            return False
        else :
            return True
    return True


def initDictionaries(DICT_DIR):
    # Create a dictionay of the tasks, callable by name of taks
    # and return
    static.init()
    # Initialize Tasks
    TASK_DIR = DICT_DIR + '/' + 'tasks'
    for filename in os.listdir(TASK_DIR):
        taskPath = TASK_DIR+ '/' + filename
        with open(taskPath, 'r') as fptr:
            t       =   fptr.read()
            task    =   json.loads(t, object_hook=Task.object_decoder)
            static.tasks[task.name] = task
        # Validate tasks, print out htose that pass, and exit if problem
    for task in static.tasks.values():
        if not checkTaskList(task.taskList):
            print("Unknown task in: %s" % ' '.join(map(str, task.taskList)))
            sys.exit(0)
