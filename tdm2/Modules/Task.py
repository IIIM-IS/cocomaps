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
    def __init__(self, name, module, canBeActivated, requiredData, conclusiveAction,
                 failureAction, timeOutAction, maxDuration, whatAmIDoing,
                 isActive, taskList, activeTasks):
        self.name             = name
        self.module           = module
        self.canBeActivated   = canBeActivated
        self.requiredData     = requiredData
        self.conclusiveAction = conclusiveAction
        self.failureAction    = failureAction
        self.timeOutAction    = timeOutAction
        self.maxDuration      = maxDuration
        self.whatAmIDoing     = whatAmIDoing
        self.isActive         = isActive
        self.taskList         = taskList
        self.activeTasks      = activeTasks



    # Each element in the Task must be defined here for saving and loading to work
    @staticmethod
    def object_decoder(obj):
        if '__type__' in obj and obj['__type__'] == 'Task':
             return Task(obj['name'],          obj['module'],
                         obj['canBeActivated'],
                         obj['requiredData'],  obj['conclusiveAction'], 
                         obj['failureAction'], obj['timeOutAction'],    
                         obj['maxDuration'],   obj['whatAmIDoing'],
                         obj['isActive'],      obj['taskList'], 
                         obj['activeTasks'])
        return obj

# If invoked directly, create a sample task and put it in the main directory

if __name__ == "__main__":
   o = json.loads('{"__type__":"Task", \
                    "name"            :"FIND-SOMETHING-TODO-1", \
                    "module"          :"YTTM", \
                    "canBeActivated"  :"Fals", \
                    "requiredData"    :["head-motor-on"],  \
                    "conclusiveAction":"(Head-Move(-90,10))", \
                    "failureAction"   :"Report-Motor-Compliance-Fail", \
                    "timeOutAction"   :"Report-Motor-Compliance-Fail", \
                    "maxDuration"     :"1000", \
                    "whatAmIDoing"    :"Lost in Space", \
                    "isActive"        :"False", \
                    "taskList"        :["HeadTurnLeft","HeadTurnRight","HeadFacingForward"], \
                    "activeTasks"     :["AskForInput"]}',
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

def createTaskList():
    # Create a dictionay of the tasks, callable by name of taks
    # and return
    static.init()
    TASKS_DIR = 'task'
    for filename in os.listdir(TASK_DIR):
        taskPath = TASK_DIR + '/' + filename
        #print(taskPath)
        with open(taskPath, 'r') as fptr:
            t       =   fptr.read()
            task    =   json.loads(t, object_hook=Task.object_decoder)
            static.tasks[task.name] = task
        # Validate tasks, print out htose that pass, and exit if problem
    for task in static.tasks.values():
        if not checkTaskList(task.taskList):
            print("Unknown task in: %s" % ' '.join(map(str, task.taskList)))
            sys.exit(0)
