#!/usr/bin/python2.7
"""
Author
    david@iiim.is

About 
    The Nunce module takes care of talking to the Nuance object in 
    psyclone space. 
    Nuance is word-to-text and text-to-word interpreter. The objective
    here is to either retrieve an output if the TDM request it, or 
    send an output if the TDM request it.
"""
import logging
from threading import Thread

class Nuance(Thread):
    """
    Connector with the Nunce object in psyclone
    """
    def __init__(self):
        # Setup debug mode
        Thread.__init__(self)

        self.logger = logging.getLogger(__name__)
        self.logger.info("Started Nuance connector")

        self.start()

    def write(self, line):
        #TODO Connect to nuace

        #DEBUG
        self.logger.debug("Sending line to nuance: \n \t\t{}".format(line))
        print line

    def read(self):
        """
        Read the Nuance input buffer. Note, person might still be talking
        deciding on whether robot should talk is defined in the TDM with
        TDM
        """
        self.logger.debug("Reading nuance buffer")

        #TODO Connect to Nuance
        temp = raw_input("\nNUNCA DEBUG MODE:\n\tENTER ANSWER: ")
        self.logger.debug("Nuance input: \n\t\t{}".format(temp))

    def tester(self):
        self.write("This is output number 1")

        self.read()



