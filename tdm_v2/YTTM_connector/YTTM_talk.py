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
    def __init__(self):
        """
        Start thread immediately with threading. This thread updates and return
        values from the yttm as requested. 
        """


        self.logger = logging.getLogger(__name__)
        self.logger.info("Started YTMM_talk")

        Thread.__init__(self)
        self.daemon = True

        self.my_turn = False
        self.P1_urn = False
        self.P2_turn = False
        self._continue = True
        # Definition of various talking variables
        self.started_talking = 0
        self.talking = False
        self.global_start = timer()
        self.check_for_turn = True
        self.my_turn_start = 0
        self.start()

    def run(self):
        """
        Actual running system for the YTTM module
        """

        # DEBUG
        count = 0
        while(self._continue):
            self.set_turns()
            time.sleep(.01) 

            # Debug
            time.sleep(.75)

    def set_turns(self):
        """
        Ask the YTTM module whos turn it is. This will probably be done 
        by querying psyclone. 
        """
        # TODO Create definitions and figure out how to make this work 

        if self.check_for_turn == True:
            if timer()- self.global_start > .5:
                self.my_turn = True
                self.logger.info("Set myTurn to true")
                self.check_for_turn = False

    



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

