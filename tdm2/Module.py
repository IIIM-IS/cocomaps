# Module.py
#
# provide a module for the tdm which monitors tasks for a particular sub-component, i.e. YTTM, 
# Face Recognition etc. 
#
# Started by: tdm.py
# Author: jacky mallett (c) IIIM
# Reviewed : David Orn : david@iiim.is

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
          # Ensure that the neccesary requiredData exists
          print(self.task.requiredData)
          # If the module data does exist
          if self.requiredData(static.tasks[self.task.taskList[self.nextSubTask]]):
              self.nextSubTask  += 1
          
              if self.nextSubTask >= len(self.task.taskList) :
                 self.nextSubTask = 0
        
              self.activeSubTask = static.tasks[self.task.taskList[self.nextSubTask]]
              self.startTime = getMillis()
          else : 
              print( self.name + " Data :" + self.task.requiredData + " not found")

      # Set task provided as the main task currently running for this module.
      # will be ignored if there is a currently running task, unless preempt is set to true
      def newTask(self, task, preempt):
          if self.task == None or preempt:
             self.task = task
             self.activateNextSubTask()

             self.status     = "ACTIVE"
             self.startTime  = getMillis()
          else:
             print self.name + " running: " + self.activeSubTask.name + self.status
      
      # Check module if requiredinfo is availible, for initial debugging we set data to 
      # false, this should be run through demo 1. 
      # True is assuming that the required data is available

      def requiredData(self, task):
          # Check if the required data is available from the psyclone message board
          if task.requiredData in self.dataAvailible():
              return True
          return False


      def dataAvailible(self):
          # Return availible data from the module, returns a list of data availible 
          # from psyclone. 
          # Todo : Connect to psyclone, centralize message board
          out = []
          # Demo 1 uses the search action an this can therefore be set as 
          if self.name is "YTTM":
              out = "[head-motor-on]"
          # This method is for debugging using positive data
          elif self.name is "MEX": # Special debugging for mex
              out = "None"
          
          return out
