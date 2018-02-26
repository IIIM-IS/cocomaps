#:''/usr/bin/python2.7
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

# Logging imports
import logging
import tdm_logger

# Projects specific imports
from Objects import Objects
from Algorithms import TDM_queues
from Algorithms import Word_Bag


class TDM(object):
    """
    Control sequence for the main objective. 
    """
    def __init__(self):
        tdm_logger.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting TDM")

        # Initializing objects, need to create new tasks.
        self.obj = Objects.Objects()
        # Initialize word bag
        self.WB = Word_Bag.Word_Bag()

        # Initialize objects
        self.task_queue = TDM_queues.Task_queue(self.obj, self.WB)

        # Initialize variables
        self.new_msg = False
        self.greeted = False
        self.start_time = timer()

        # Add other information 
        self.create_version()


    def run(self):
        """
        General run method. Called from top level each time it is my turn
        i.e. YTTM gives turn to robot
        """
        if timer() - self.start_time > 1 and self.WB.new_words:
            if not self.greeted:
                # Put new task onto stack
                self.task_queue.insert_task({"Type":"Tasks","Name":"greet"})
                self.greeted = True
                self.start_time = timer()

            _dict = self.task_queue.run()

            if _dict["Result"] == "out_msg":
                return _dict["Text"]
            if  _dict["Result"] == "new_task":
                self.task_queue.insert_task({"Type":"Tasks", "Name":_dict["Name"]})
            elif _dict["Result"] == "Task_queue:Empty":
                self.logger.info("Emptied queue")
            elif _dict["Result"] == "Action_stack:Empty":
                self.logger.info("Emptied action stack")

            if self.task_queue.isEmpty():
                # If task queue is emptied then ask again for a new objective 
                # to complete
                self.task_queue.insert_task({"Type":"Tasks", "Name":"get_objective"})


    def input_text(self, input):
        """
        Add text from Nuance into the word bag and store until used
        """
        self.WB.add(input)

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
        print "\tMEx"
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
    obj.WB.new_words = True
    T=timer()
    while timer()-T < 1:
        pass
    obj.run()
