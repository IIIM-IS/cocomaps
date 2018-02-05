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
    def __init__(self, api=None):
        # Setup debug mode
        Thread.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Started Nuance connector")
        self.daemon = True
        self.start()

        self.word_buffer = None
        
        # Set a connector (psyclone) 
        if api :
            self.api = api
        else :
            self.api = None



    def write(self, line):
        """
        Write a string line to Nunace so the robot can say something to 
        the user
        """
        #TODO Connect to nuace
        
        #DEBUG
        self.logger.debug("Sending line to nuance: \n \t\t{}".format(line))
        # TODO : THOR, connect to psyclone
        if self.api:
            while( self.api.ShouldConinue() ):
                # Set the Nuance output variable
                self.api.post(line)
                # Wait for sentence to finish
                # Check if sentence finished ok
                while( self.api.read_data("Still Talking") ):
                    None
                ok = self.api.read_data("NunaceFinishedOKVariable")




    def read(self):
        """
        Read the Nuance input buffer. Note, person might still be talking
        deciding on whether robot should talk is defined in the TDM with
        TDM
        """
        # Current raw method, clear word_buffer and get new input. Future
        # methods, store words to get a good understanding where the discussion
        # is going, use words to create probability function and run methods
        self.word_buffer = None

        self.logger.info("Reading nuance buffer")
        if self.api:
            # TODO : THOR, how to read from psyclone
            read_data = self.api.GetSomeThingOrAnother("FromThisVariable")
        else :
            # Debug method, input in keyboard input form
            read_data = raw_input("\nNUANCE: DEBUG MODE:\n\tENTER ANSWER: ")
            self.logger.debug("Nuance input: \n\t\t{}".format(read_data))

        
        # TODO the Python-Nunace output must be a set, now a string, i.e.
        # turn a string into a array of words to process. Array of one is
        # okay
        self.word_buffer = read_data.lower().split(" ")
        return self.word_buffer
