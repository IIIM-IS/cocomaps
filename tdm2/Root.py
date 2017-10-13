#Root.py
# Part of cocomaps project. This creates a root for the tasks needed to 
# perform. The tasks are defined in the folder task/ and they are created
# using the Task.py module. 
# Here we create a root for the decision tree, inside a task are links
# to next tasks, defined in taskList. 
# Started by: tdm.py 
# Reviewed : David Orn : david@iiim.is

from threading import Thread
import time

# Get current time in milliseconds
def getMillis():
    return int(round(time.time()*1000))


class Crawler(Thread):
    # A net crawler, initiated by Root class that runs down the
    # query tree and hands out actions based on tree struct
    def __init__(self, tasks):
        Thread.__init__(self)

        self.taskList   = tasks.taskList
        self.noTasks    = len(task.taskList)
        self.Finished   = False
        self.actionItems= len(task.taskList)
    

# Create a root for the tree
class Root():
    def __init__(self, task):
        self.name       = "ROOT:"+task.name 
        # A root has a starting task that needs to be defined
        self.taskList   = task.taskList 
        self.taskListLen= len(task.taskList)
        self.task      = task
        self.status     = "INACTIVE"
        self.debugCount = 1 # Debug counter used in psycloneData
        self.staticTasks = None
    
    # Add the entire list of tasks availible, i.e. the static
    # list of possible tasks
    def setStaticTasks(self, tasks):
        print(tasks)
        self.staticTasks = tasks
        
    def printTasks(self):
        for i in self.staticTasks:
            print(i)

    #TODO: Need to be able to get task by name
    #TODO: Start crawler by connecting task to template.?How to impliment templates
    #TODO: Crawler returns root!

    def runFromRoot(self):
        # Start from the tasks in root, try to run them
        pass

