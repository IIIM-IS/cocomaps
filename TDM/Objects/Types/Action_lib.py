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

def write_to_buffer( _dict):
    """
    Return a object
    """
    logger.debug("Creating a msg")
    if _dict["msg"] == "speak":
        msg = cmsdk2.DataMessage()
        logger.debug("Adding string msg: '{}'".format(_dict["out_msg"]))
        msg.setString("OutputMsg", _dict["out_msg"])
        return {"Result":"out_msg", "Text":msg}


def new_task( _dict):
    """
    Start a new task with the input dict
    """
    return {"Result":"new_task", "name":_dict["keyword_result"]}
    


def resolve_pass( _dict):
    """
    Solve the pass action of the task
    """
    pass

def start_screen_navigation( _dict):
    """
    Start a screen navigation task
    """
    return {"Result":"new_task", "name":"screen_navigation"}


def get_objective( _dict):
    """
    Get specific objective
    """
    return {"Result":"new_task", "name":"get_objective"}



def move_menu( _dict):
    """
    Navigate through the menu system. 
    """


action_dict = {
    "write_to_buffer":write_to_buffer,
    "new_task":new_task,
    "resolve_pass":resolve_pass,
    "start_screen_navigation":start_screen_navigation,
    "get_objective":get_objective,
    "move_menu":move_menu,
}

