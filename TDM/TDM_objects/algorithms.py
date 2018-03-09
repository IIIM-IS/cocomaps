#! /usr/bin/env python
#################################################################################
#     File Name           :     TDM_algorithms.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-07 10:16]
#     Last Modified       :     [2018-03-09 09:56]
#     Description         :     Algorithms specifically pertaining to the
#                               Supervisory Intermediate for the task dialog 
#                               manager
#     Version             :     0.1
#################################################################################

import logging
from objects import *

class TDM_base(object):
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.stack   = []
        self.history = []
        self.len     = 0

    def isEmpty(self):
        if self.stack == []:
            return True
        return False 

    def length(self):
        return self.len
    
    def pop(self):
        if self.stack != []:
            temp = self.stack.pop(0)
            self.logger.debug("Popping item from action stack: {}".format(temp.type))
            return temp

    def top(self):
        if self.stack != []:
            return self.stack[0]


    def reset(self):
        self.len = 0
        self.stack = []

class TDM_AA(TDM_base):
    """
    Supervisory Intermediate Active Action stack

    Monitors the active actions and flags them if they finish, throws error 
    if not finished.
    """
    #TODO expand this to be able to monitor action tasks that have been 
    # "sent out" of the system.
    def __init__(self):
        TDM_base.__init__(self,"TDM_AA")
        self.logger.debug("TDM_AA created")

    def add(self, action):
        self.stack.append(action)

    def wait(self):
        for action in self.stack:
            if action != None and not action.elapsed():
                self.logger.info("Action {}, wait for {} sek, remaining {}".format(
                    action.type,
                    action.max_time,
                    action.remaining()
                ))
                return True
        return False 
    
    def timeout(self):
        for action in self.stack:
            if action.timeout_check():
                return True
            return False


class TDM_SS(TDM_base):
    """
    Supervisory Intermediate Speak Stack TDM_SS, put things that the system 
    wants to say onto the stack. 
    """
    def __init__(self):
        TDM_base.__init__(self,"TDM_SS")
        self.logger.debug("TDM_SS created")

    def add(self, sentence, task_id):
        talk_obj = Talk_object()
        talk_obj.set_string(sentence, task_id)

        self.stack.append(talk_obj)


    def pop(self):
        """
        Remove speak object from the stack
        """
        if not self.isEmpty():
            temp = self.stack.pop(0)
            self.logger.debug("Removed object from speak stack")
            return temp

class TDM_AS(TDM_base):
    """
    Supervisory Intermediate Action Stack TDM_AS. Control flow over
    actions to be performed.
    """
    def __init__(self, active_stack):
        TDM_base.__init__(self,"TDM_AS")
        self.logger.debug("TDM_AS created")
        self.active_stack = active_stack

    def add(self, object):
        """
        Add object from this file to the action stack. 
        """

        self.history.append(object.type)
        self.logger.debug("Adding object to stack: {}".format(object.type))
        self.stack.append(object)
        self.len+= 1

    def pop(self):
        if not self.isEmpty():
            temp = self.stack.pop(0)
            temp.start_timer()
            self.active_stack.add(temp)
            return temp


