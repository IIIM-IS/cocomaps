#!/usr/bin/python2.7
"""
26.01.18
Author 
    david@iiim.is

Objective
    Connect to the yttm module and query it using threads to minimize lag between
    updated values and perceived values. The module needs to query the psyclone
    workspace about selective parameters, specifically, whose turn is it.
"""

from threading import Thread
from timeit import default_timer as timer
import logging
import time


class YTTM_talk(Thread):
    """
    Constantly monitor and update what the YTTM is doing
    """
    def __init__(self, api=None):
        """
        Start thread immediately with threading. This thread updates and return
        values from the yttm as requested. 
        """
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Started YTMM_talk")

        self.who_am_i = "Debug"

        self.api = api



    def check_whos_turn(self):
        """
        Ask the YTTM module whos turn it is. This will probably be done 
        by querying psyclone. 
        """

        if self.api:
            #TODO : Thor, implement connection to YTTM via psyclone
            pass

        return 0



    def starting_talking(self):
        """
        Monitor how long it takes to output a audio signal, this value can
        then be accessed to assess if the output is taking to long
        """
        self.talking = True
        self.started_talking = timer()
    
    def talking_time(self):
        """
        Return a value that says how long the system has been talking_time
        """
        if self.talking == True:
            return timer()-self.started_talking
        else:
            return 0

