# Module.py
#
# provide a module for the tdm which monitors tasks for a particular sub-component, i.e. YTTM, 
# Face Recognition etc. 
#
# Started by: tdm.py
# Author: jacky mallett (c) IIIM

from threading import Thread
import time
import static

# Status: ACTIVE : INACTIVE : TIMEOUT : ERROR

# Get current time in milliseconds
def getMillis():
    return int(round(time.time() * 1000))

class Module(Thread):
      def __init__(self, name):
          Thread.__init__(self)
          self.name          = name			# Name of module
          self.task          = None
          self.activeSubTask = None
          self.nextSubTask   = 0
          self.status     = "INACTIVE"
          self.daemon     = True
          self.sleepTime  = 0.1
          self.startTime  = -1

      # Main loop of Thread
      def run(self):
          while True:
             if(self.activeSubTask == None):
                print "\033[94m" + self.name + ": No current task" + "\033[00m"
             else:
                if(getMillis() - self.startTime > int(self.activeSubTask.maxDuration)):
                   self.activateNextSubTask()
                else:
                   print self.name + ": " + self.activeSubTask.name
             time.sleep(self.sleepTime)

      # Switch to the next subtask in the list
      #  - todo: remove loop over subtasks for demonstrations
      def activateNextSubTask(self):
          self.activeSubTask = static.tasks[self.task.taskList[self.nextSubTask]]
          self.startTime = getMillis()
          self.nextSubTask  += 1
          
          if self.nextSubTask >= len(self.task.taskList) :
               self.nextSubTask = 0

      # Set task provided as the main task currently running for this module. 
      # will be ignored if there is a currently running task, unless preempt is set to true
      def newTask(self, task, preempt):
          if self.task == None or preempt:
             self.task = task
             self.activateNextSubTask()

             self.status     = "ACTIVE"
             self.startTime  = getMillis()
          else:
             print self.name + " running: " + self.activeSubTask.name 






      
