#!/usr/bin/python2.7
"""
08.02.18
Author
    David Orn Johannesson | david@iiim.is
Objective
    Control sequence for dialogue of the CoCoMaps project.
"""


import os
from timeit import default_timer as timer
import json
import re

# Logging imports
import logging
import tdm_logger

# Projects specific imports
from MEx import MEx
from Objects import Objects
from Algortihms import TDM_queues


class TDM(object):
    """
    Control sequence for the main objective. 
    """
    def __init__(self):
        tdm_logger.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting TDM")

        # Initializing objects, need to create new tasks.
        self.obj =  Objects.Objects()

        # Initialize objects
        self.task_queue = TDM_queues.Task_queue(self.obj)

        # Initialize variables
        self.new_msg = False
        self.greeted = False
        self.start_time = 0

        # Add other information 
        self.create_version()


    def run(self):
        """
        General run method. Called from top level each time it is my turn
        i.e. YTTM gives turn to robot
        """
        debug_count =  0
        while True and debug_count < 10:
            if not self.greeted:
                # Put new task onto stack
                self.task_queue.insert_task({"Type":"Tasks","Name":"greet"})
                self.greeted = True
                self.start_time = timer()

            _dict = self.task_queue.run()

            if _dict["Return"] == "Question":
                pass
            elif _dict["Return"] == "NewTask":
                pass
            elif _dict["Return"] == "Debug":
                print "Returned debug value"
            elif _dict["Return"] == "Task_queue:Empty":
                print "Task queue emptied"
            elif _dict["Return"] == "Action_stack:Empty":
                print "Task queue emptied"




            if self.task_queue.isEmpty():
                self.task_queue.insert_task({"Type":"Tasks", "Name":"get_objective"})

            debug_count += 1
            print debug_count



# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  
# * * * * * * * * *     SOME DECENT HELP FUNCTIONS      * * * * * * * * * * * *  
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  

    def q_str(self, task):
        """
        Return random string from task.out_strings for output
        """
        if task.out_strings:
            return task.out_strings[
                np.random.randint(0,len(task.out_strings)+1)
            ]
        return []


    def elapsed(self):
        """
        Helper function for getting time elapsed since self.start_time
        was called last
        """
        if self.start_time != 0:
            return timer()-self.start_time()
        return 0
            


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * * OTHER FUNCTIONS USED FOR INFORMATION  * * * * * * 
# * * * * * * * *         SHARING PURPOSES.             * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

    def print_available(self):
        """
        Print all available types and objects within structure
        """
        self.task_queue.print_available()

    def create_version(self):
        """
        Get information about the current iteration version, 
        what is active and what needs more work
        """
        current_folder = os.getcwd().split('/')[-1]
        tdm_version_file = "TDM_version.json"
        if current_folder != "TDM":
            tdm_version_file = "TDM/"+tdm_version_file
            
        with open(tdm_version_file, 'rb') as fid:
            data = fid.read()
            data = json.loads(data)
        self.data = data    
        self.version = data["Version"]

    def version_notes(self):
        """
        Print out the version notes for TDM
        """
        print 70*'*'
        print "\t\tVersion notes"
        print 70*'*'
        print "Author \t\t: {}".format(self.data["author"])
        print "Version no\t: {}".format(self.data["Version"])
        print "Release date\t: {}".format(self.data["Release"])
        print "Stable\t\t: {}".format(self.data["Stable"])
        print "Active modules"
        print "\tMEx\t: {}".format(self.data["MEx"])
        print "Available objects"
        for obj in self.data["objects"]:
            print "\t {}".format(obj)
        print "Author release notes"
        print "\t{}".format(self.data["Notes"])
        print 70*'*'
        print 70*'*'


if __name__ == "__main__":
    obj = TDM()
    obj.version_notes()
    obj.print_available()
    print 10*'*/ '
    print "Starting run..."
    print 10*'*/ '
    obj.run()
