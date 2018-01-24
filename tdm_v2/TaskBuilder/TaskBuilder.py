#!/usr/bin/python2.7
"""
24.01.18
Author
    david@iiim.is

Objective
    Tasks in the cocomaps project define the structure of actions that can 
    be performed. Tasks incorporate information that is needed to move onto
    the next task, or send specific instructions to a source.
"""

import json, os, logging


class TaskBuilder(object):
    """
    Using an object stucture to store the json built tasks
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Started Task builder")
