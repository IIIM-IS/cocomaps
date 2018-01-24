#!/usr/bin/python2.7
"""
24.01.18
Author
    david@iiim.is

About
    The meaning extractor takes in a sentance or a set of words and tries to 
    map them to specific output responses. 
"""

import logging



class MEx(object):
    """
    Meaning extractor object, called in the beginning of the tdm and stored
    in background. Uses various specially constructed dictionaries
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Starting up MEx")

