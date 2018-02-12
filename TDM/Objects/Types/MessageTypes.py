#!/usr/bin/python2.7
"""
08.02.18
Author 
    David Orn Johannesson : david@iiim.is

Objective
    Write a set of message types connected to the cmsdk2 library so that 
    the outputs, if of the right kind can be sent and handled correctly
"""

import cmsdk2
import logging

logger = logging.getLogger("Action_Lib")
def talk_message(_dict):
    logger.info("Creating talk message")
    logger.info("\t{}".format(_dict["output_msg"]))
    msg = cmsdk2.DataMessage()
    msg.setString(_dict["output_msg"])

    return msg
        
    
