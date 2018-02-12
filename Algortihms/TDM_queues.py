#! /usr/bin/env python
#################################################################################
#     File Name           :     Algortihms/TDM_queues.py
#     Created By          :     David Orn Johannesson
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-09 11:47]
#     Last Modified       :     [2018-02-12 13:23]
#     Description         :     TDM specific algorithm approaches and 
#                                   types.
#     Version             :     0.1
#################################################################################
import logging


from MEx import MEx
import copy
logger = logging.getLogger("Algorithms")

class Task_queue(object):
    """
    A FFO queue specifically for Tasks types objects. Tasks can create new
    tasks but a task must be finished for next task to start
    """
    def __init__(self, object_reference):
        """
        Create an empty queue
        inputs
            object_reference :  A pointer to the object type dictionary
                            containing definitions of objects
        """
        logger.debug("Creting empty task queue")
        self.task_list = []
        self.iter_count = 0

        self.MEx = MEx.MEx()
        self.Objects = object_reference
        self.AS = Action_stack(object_reference)
        

    def isEmpty(self):
        """
        Check if list is empty
        """
        if self.task_list:
            return False
        return True


    def insert_task(self, _dict):
        """
        Insert new task at the back of the list
        """
        assert _dict["Type"] == "Tasks", ("Insert error, type not Task")
        new_task = self.Objects.new_object(_dict)
        self.task_list.append(new_task)
        _dict["Parent"] = new_task

        # This function is called each time a new task is created
        # this means that the objects dictionary is inside the _dict
        for action in new_task.action:
            _dict["Type"] = "Actions"
            _dict["Name"] = action
            self.AS.insert(_dict)


    def run(self):
        """
        Main functino. Tries to run the task by trying to run each task
        first. If a task is met the action is popped of the Action_stack. 
        If all actions are finished the task is popped of the Task_queue
        """
        if not self.isEmpty():
            if not self.AS.isEmpty():
                logger.debug("Running top task : {}".format(
                                        self.task_list[0].name))
                return self.AS.run()
            else : 
                self.pop()
                return {"Return":"Task_queue:Popped"}
        else:
            return {"Return":"Task_queue:Empty"}


    def pop(self):
        """
        Remove front task from list
        """
        if not self.isEmpty():
            self.task_list.pop(0)

    def __iter__(self):
        return self

    def next(self):
        if self.iter_count >= len(self.task_list):
            self.iter_count = 0
            raise StopIteration
        ret_val = self.task_list[self.iter_count]
        self.iter_count += 1
        return ret_val

    def print_stack(self):
        """
        Print out the task stack currently un use
        """
        print "Tasks in queue :"
        for task in self.task_list:
            print "\t{}".format(task.name)


    def examine_stacks(self):
        self.print_stack()
        self.AS.print_stack()

    def print_available(self):
        """
        Print available objects from the MEx object
        """
        self.MEx.print_available()

class Action_stack(object):
    """
    A stack for actions to be handled. Tasks are required to call actions
    and a task can put actions on the action stack. 
    inputs
        object_reference : Same as with Task_queue, i.e. pointer to the
                        object that contains information and rules about
                        the Objects
    """
    def __init__(self, object_reference):
        self.stack = []
        self.iter_count = 0
        self.Objects = object_reference

# * * * * * * * * * * * * * * * * * * * * * 
# * * * * * MAIN OBJECTIVE RUN  * * * * * * 
# * * * * * * * * * * * * * * * * * * * * * 
    def run(self):
        """
        Main objective function. Calls the relevant function, 'handles' 
        various errors through the dictionary object.
        """
        if self.stack:
            action = self.stack[0]
            _dict = {}
            _dict["Task"] = action.parent
            return action.run()

        else:
            return {"Results":"Action_stack:Empty"}



# * * * * * * * * * * * * * * * * * * * * * 
# * * * * * END OF MAIN OBJECTIVE * * * * * 
# * * * * * * * * * * * * * * * * * * * * * 

    def isEmpty(self):
        if self.stack:
            return False
        return True

    
    def insert(self, _dict):
        """
        Insert a new action onto action stack. 

        inputs
            _dict   = Python dictionary with following attributes
                Action = action object to be put onto stack
                q_str  = if Action.question==True then q_str is 
                            available as output question string
        """

        action = self.Objects.new_object({"Type":"Actions", 
                                          "Name":_dict["Name"]})
        action.parent = _dict["Parent"]
        
        assert action._type == "Action"

        if self.isEmpty():
            self.stack.append(action)
        else:
            self.stack.append(action)


    def pop(self):
        if not self.isEmpty():
            return self.stack.pop(0)
        else :
            return None

    def print_stack(self):
        """
        Print out current action stack
        """
        print "Action stack :"
        for action in self.stack:
            print "\t\t{}".format(action.name)

# * * * * * * * * * * * * * * * * * * * * * * * * * * 
# * * * * * * * FUNCTIONS FOR ITERATION * * * * * * *
# * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __iter__(self):
        return self

    def next(self):
        if self.iter_count >= len(self.stack):
            self.iter_count = 0 
            raise StopIteration
        ret_val = self.stack[self.iter_count]
        self.iter_count += 1
        return ret_val
    