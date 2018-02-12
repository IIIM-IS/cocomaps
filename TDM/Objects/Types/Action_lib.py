#!/usr/bin/python2.7
"""
02.01.18
Author 
    David Orn : david@iiim.is
Objective
    Create a library for all possible actions that can be performed. 
    There are two types of actions. 
                Local   = Happening on the robot in conversation
                Remote  = Happening on the robot in motion
    The action function decides which is which. The context of the action
    should reveal which it should do. 
"""

import numpy as np
import cmsdk2
import logging
import MessageTypes
logger = logging.getLogger("Action_lib")

def write_to_buffer(self, _dict):
    """
    Return a object
    """
    logger.debug("Creating a msg")
    if _dict["msg_type"] == "speak":
        return MessageTypes.talk_message(_dict)


def new_task(self, _dict):
    """
    Start a new task with the input dict
    """
    # TODO : Implement methodology
    pass


def resolve_pass(self, _dict):
    """
    Solve the pass action of the task
    """
    pass


action_dict = {
    "write_to_buffer":write_to_buffer,
    "new_task":new_task,
    "resolve_pass":resolve_pass
}
