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

from prerequisites import *
from Task import * 
from actions import * 
from InfoBag import *
import static as static

import logging

logger = logging.getLogger(__name__)

class TaskHandler():
    def __init__(self, task):
        self.task  = task
        self.task.isActive = 1
        self.deamon = True
    # Main function for running a task

    def run(self):
        logger.info("Running task: " + self.task.name)
        # First step of task protocol, ensure prerequisites
        test = True
        logger.debug("Name of prerequisites")
        logger.debug(",".join(self.task.prerequisites))
        for prereq in self.task.prerequisites:
            logger.debug("Prerequisites test: " + prereq)
            test, errMsg = self.prerequisites(prereq)
            if not test:
                # If the prerequisite fails it should stop the
                # for loop and test==False so it does not go 
                # into the next statement
                logger.debug(prereq + " : FAILED")
                break
        logger.debug("Prereq test after testing: " + str(test))
        if test: 
        # Positive test
            taskTest = True
            for taskName in self.task.taskList:
                newTask = static.tasks[taskName]
                newTaskHandler = TaskHandler(newTask)
                logger.debug("Starting new task: " + newTaskHandler.task.name)
                taskTest, errMsg = newTaskHandler.run()
                if not taskTest:
                    logger.debug("Subtask failed: " + errMsg)
                    return taskTest, errMsg

            if taskTest:
                for function in self.task.functionCalls:
                    logger.debug("Running function: " + function) 
                    print(self.task.name)
                    funcTest, errMsg = actions[function](self.task)

                    if not funcTest:
                        return funcTest, errMsg
        logger.debug("True;  Finished :" + self.task.name)
        return True, ""




    def prerequisites(self, prereq):
        test = True
        errMsg = ""
        test = prerequisites[prereq]([])
        if not test: 
            errMsg = "\tFailed TaskHandler:prerequisites:checkPrerequisites for " + self.task.name + " - " + prereq
        logger.info(str(test) + errMsg)
        return test, errMsg




if __name__ == "__main__":
    initDictionaries(".") # This might be a problem...
    testTaskName = 'FIND-SOMETHING-TODO-1'
    testTask = static.tasks[testTaskName]
    
    testHandler = TaskHandler(testTask)
    res, reason = testHandler.run([])
    if res:
        print("Successful")
    else :
        print(reason)
