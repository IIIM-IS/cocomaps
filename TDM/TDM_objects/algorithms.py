#! /usr/bin/env python
#################################################################################
#     File Name           :     TDM_algorithms.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-07 10:16]
#     Last Modified       :     [2018-03-28 13:17]
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
        return len(self.stack)

    def pop(self, id=0):
        if self.stack != []:
            temp = self.stack.pop(id)
            self.logger.debug("#TDM: Popping item from action stack: {}".format(temp.type))
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
        self.logger.debug("#TDM: TDM_AA created")
        self.stack_id = []


    def add(self, action):
        self.stack.append(action)
        self.stack_id.append(action.id())


    def wait(self):
        # <12.04.18> If there is an active hold action on the
        # active actions stack, wait until it is popped
        if self.isEmpty():
            return False
        for action in self.stack:
            if action.get_holds() is True:
                self.logger.debug("TDM_AA: wait(True)")
                return True
                #if action is not None and not action.elapsed():
                # <12.04.18> Comment out, not necessary
                #self.logger.info("Action {}, wait for {} sek, remaining {}".format(
                #    action.type,
                #    action.max_time,
                #    action.remaining()
                #))
                #    return True
        return False

    def timeouts(self):
        for action in self.stack:
            if action.timeout_check():
                return True
            return False
    def print_stack(self):
        out_str = ""
        if self.stack != []:
            for val in self.stack:
                out_str += "{} {} {} \n".format(val.type, val.id(), val.msg)

        if out_str != "":
            return out_str
        return "Active actions are empty"

    def add_finished_id(self, id):
        # Remove action from active action stack once id is returned from psyclone
        if self.stack_id != []:
            if id in self.stack_id:
                loc = self.stack_id.index(id)
                self.logger.debug("#TDM : finished id: {}, ids in stack {}, {}".format(
                    id, self.stack_id, self.stack
                ))
                action = self.stack.pop(loc)
                self.stack_id.pop(loc)
                self.logger.debug("#TDM: Removing from AA {} - {} | left {}".format(action.type,
                                                                              action.msg,
                                                                         len(self.stack)))

"""
    def add_finished_id(self, id):
        We must, temporarily simply pop the value that is on the stack.
        We are having some issues with storing the value IDs
        self.logger.debug('#TDM: Would Remove from AA {};'
                          'still on stack {}'.format(id, self.stack))
        if self.stack is not []:
            if self.stack is None:
                pass
            else:
                self.stack.pop(0)
"""

class TDM_SS(TDM_base):
    """
    Supervisory Intermediate Speak Stack TDM_SS, put things that the system
    wants to say onto the stack.
    """
    def __init__(self):

        TDM_base.__init__(self,"TDM_SS")
        self.logger.debug("#TDM: TDM_SS created")
        self.id_stack = []

    def add(self, sentence, obj, level=0, id=-1):
        put_on = True
        obj.not_asked()
        if not self.isEmpty():
            for obb in self.stack:
                if obb.msg == sentence:
                    put_on = False

        if put_on:
            talk_obj = Talk_object()
            talk_obj.set_string(sentence, id, level)
            self.stack.append(talk_obj)



    def pop(self, level=0):
        """
        Remove speak object from the stack
        """
        if not self.isEmpty():
            if level == 0:
                return self.stack.pop(0)
            else:
                for idx,val in enumerate(self.stack):
                    if val.level == level:
                        temp = self.stack.pop(idx)
                        return temp

            return None

    def print_stack(self):
        if not self.isEmpty():
            out_str = ""
            for val in self.stack:
                tempstr = val.msg + ","
                out_str = out_str + tempstr
            return str(out_str)

        else:
            return "Speech stack is empty"

    def reset(self):
        self.stack = []
        self.id_stack = []

class TDM_AS(TDM_base):
    """
    Supervisory Intermediate Action Stack TDM_AS. Control flow over
    actions to be performed.
    """
    def __init__(self, active_stack):
        TDM_base.__init__(self,"TDM_AS")
        self.logger.debug("#TDM: TDM_AS created")
        self.active_stack = active_stack

    def add(self, object):
        """
        Add object from this file to the action stack.
        """
        self.history.append(object.type)
        self.logger.debug("#TDM: Adding object to stack: {}".format(object.type))
        self.stack.append(object)


    def pop(self):
        if not self.isEmpty():
            temp = self.stack.pop(0)
            temp.start_timer()
            self.active_stack.add(temp)
            return temp


    def print_stack(self):
        out_str = ""
        if self.stack != []:
            for val in self.stack:
                out_str += "{} {} {} \n".format(val.type, val.id(), val.msg)

        if out_str != "":
            return out_str
        return "Action stack is empty"

    def instack(self, id):
        """
        Check if a value is in the stack
        """
        if self.isEmpty():
            return False
        else:
            for val in self.stack :
                if id == val.id():
                    return True

        return False
