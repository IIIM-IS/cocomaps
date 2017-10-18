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
from checkPrerequisites import *
from Task import * 
from actions import *
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
        
        if self.prerequisites():
            # Here all prerequisites are availible
            # Start by trying to run the initial actions
            for taskName in self.task.activeTasks:
                if activateTask(taskName, self.debug):
                    continue
                else :
                    errStr = "Failed: TaskHandler:run:activeTask for " + self.task.name
                    return False, errStr
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

            for function in self.task.conclusiveAction:
                if self.debug == 1:
                    print("DEBUG: TaskHandler.run():for function in self.task.conclusiveAction" + function + " -  " +self.task.name)
                funcTest, newTaskName = eval(function + "(int(" + self.task.maxDuration + "),'" +self.task.name + "')")
                if not funcTest:
                    errStr = "Failed :: TaskHandler.run(): For function " + function
                    return False, errStr
                else :
                    print(static.tasks.keys())
                    if newTaskName in static.tasks.keys():
                        print("This key is in the static task")
                    else:
                        print("This key has not been created")


        
        else : # self.prerequisites returns false, some data missing
            # If the data is missing we can't continue
            errStr = "Failed TaskHandler:run:prerequisites for " + self.task.name
            return False, errStr
        return True, "" # If task made it here, it finished well and returns True


    def prerequisites(self):
        for prereqs in self.task.requiredData:
            test, _ = checkPrerequisites(prereqs, self.debug)
            # Sends name of prerequisite function and checks if
            # that functio is availible. If one is false then return
            # false
            if test == False: 
                errStr = "Failed TaskHandler:prerequisites:checkPrerequisites for " + self.task.name + " - " + prereqs
                return False, errStr
        return True, ""


# Define ceratin task specific functions
def activateTask(*args):
    # Takes care of activation tasks, activation tasks are tasks
    # that need input from user before continuing, e.g. asking for
    # a task. Before asking for a task some prequisites need to be met
    # once they are met the task can start by asking questions etc. 
    # waiting for input and then continue to next item in taskList.
    # *args is used to be able to control the debug functionality
    debug = args[1]
    taskName = args[0]
    print("Active task name "+ taskName)
    task = static.tasks[taskName]
    tempHandler = TaskHandler(task)
    return tempHandler.run()




if __name__ == "__main__":
    createTaskList()
    testTaskName = 'FIND-SOMETHING-TODO-1'
    testTask = static.tasks[testTaskName]
    
    testHandler = TaskHandler(testTask)
    res, reason = testHandler.run()
    if res:
        print("Successful")
    else :
        print(reason)
