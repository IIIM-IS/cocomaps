#!/usr/bin/python2.7
"""
02.01.18
Author 
    David Orn : david@iiim.is
Objective
"""

import numpy as np
import logging
logger = logging.getLogger("Action_lib")

def write_to_buffer(_dict):
    """
    Return a object
    """
    return {"Result":"Talk", "msg":_dict["out_msg"]}

def new_task( _dict):
    """
    Start a new task with the input dict
    """
    action  = _dict["action"]
    p       = _dict["p"]

    return {"Internal":"new_task", 
            "name":action.keywords[np.argmax(p)]}

def start_specific(_dict):
    """
    Start the specific pass action in the task
    """
    return {"Internal":"new_task",
            "name":_dict["task"].pass_action}

def menu(_dict):
    """
    Return a keyword search for  relevant menu slection
    """
    return {"Result":"Menu", "ButtonName":_dict["action"].keywords[np.argmax(_dict["p"])]}

    
def move(_dict):
    """
    Return a name of a point that the executor should move to
    """
    action  = _dict["action"]
    p       = _dict["p"]

    return {"Result":"Move", "Point":action.keywords[np.argmax(p)]}


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
    pass


action_dict = {
    "write_to_buffer":write_to_buffer,
    "new_task":new_task,
    "resolve_pass":resolve_pass,
    "start_screen_navigation":start_screen_navigation,
    "get_objective":get_objective,
    "move_menu":move_menu,
    "move":move,
    "menu":menu,
    "start_specific":start_specific
}

