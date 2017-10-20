# TaskHandler.py 
# This is the task machine that takes in a task and does actions according
# To task definition. 
# The typical structure is 
#       1. Check for prerequisites (RequiredData)
    #       2. If prereqs return True : Check if task has activeTask if
#                   there are active tasks then run through them 
#                   active tasks are tasks that require feedback
#                   e.g. asking a question for input
#       3. Once all active tasks have returned True start running through
#                   taskList, return True on each task that has finished
#                   once all tasks in taskList have returned True return
#                   True - The task list has finished
#
# Author : David Orn = david@iiim.is
#

import time
from prerequisites import *
from Task import * 
from actions import * 
from InfoBag import *
# FOR DEBUGGING
import static as static

def getMillis(): # Get the current time in milliseconds, 
                 # used to compute the maximum allowed time.
    return int(round(time.time()*1000))


class TaskHandler():
    def __init__(self, task):
        self.task  = task
        self.debug = 0 # Debug on/off  1/0
        self.task.isActive = 1
    # Main function for running a task
    def run(self):
        print("Current task: " + self.task.name)
        # Start by running check of the prerequisites
        # run returns two values True, [] or False, locationWhereFailed
        prereqTest, errStr = self.prerequisites() 
        if prereqTest:
            # Here all prerequisites are availible
            for taskName in self.task.taskList:
                # Create a new set of tasks
                # TODO need to create a new Task based on task name and then I can create an instance of 
                # class TaskHandler with Task:task
                if self.debug == 1:
                    print("Debug : TaskHandler.run()::for taskName " + self.task.name) 
                task = static.tasks[taskName]
                print("Subtask created: "+task.name)
                newTask = TaskHandler(task)
                taskTest, newTaskName = newTask.run()
                errStr = "Failed TaskHandler:Run:newTask.run() " + task.name
                if taskTest == False:
                    return False, errStr


            # TODO fix code to match new structure;
            for function in self.task.functionCalls:
                if self.debug == 1:
                    print("DEBUG: TaskHandler.run():for function in self.task.conclusiveAction" + function + " -  " +self.task.name)
                print("Debug: function call name: " + function)
                # Run a function from actions, based on actions dictionary
                funcTest, errStr =  actions[function](self.task)
                
                if not funcTest:
                    errStr = "Failed :: TaskHandler.run(): For function " + function
                    return False, errStr
                return funcTest, errStr

        
        else : # self.prerequisites returns false, some data missing
            # If the data is missing we can't continue
            return False, errStr
        return True, "" # If task made it here, it finished well and returns True


    def prerequisites(self):
        test = True
        errStr = ""
        for prereqs in self.task.prerequisites:
            test = prerequisites[prereqs]([])
            # Sends name of prerequisite function and checks if
            # that functio is availible. If one is false then return
            # false
            if not test: 
                errStr = "Failed TaskHandler:prerequisites:checkPrerequisites for " + self.task.name + " - " + prereqs
                break
        return test, errStr




if __name__ == "__main__":
    initDictionaries("") # This might be a problem...
    testTaskName = 'FIND-SOMETHING-TODO-1'
    testTask = static.tasks[testTaskName]
    
    testHandler = TaskHandler(testTask)
    res, reason = testHandler.run()
    if res:
        print("Successful")
    else :
        print(reason)
