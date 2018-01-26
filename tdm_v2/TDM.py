#!/usr/bin/python2.7
"""
Author
    david@iiim.is

About 
    Task Dialog(ue) Manager (TDM) for CoCoMaps project, a collaborative project
    with CMLabs and IIIM. The manager controls high level (course granular 
    timing) decision as well as giving instructions to the robot. 
"""
# Standard modules
import os
import time

# Custom modules
from MEx import MEx
from Tasks import TaskHandler
from YTTM_connector import YTTM_talk
from Nuance import Nuance

# # # # # # DEBUG : CLEAN LOGGING FOLDER
os.system("find Logging/ -name *.log -exec rm {} \;")

# # # # # # DEBUG : END OF DEBUG

# Setup the logging module for getting, setting and storing information
import logging
import Logging.tdmLogging


class TDM(object):
    """
    The main task dialog object used to connect and interface with 
    pysclone
    """
    def __init__(self):
        # Start by defining the loggers
        Logging.tdmLogging.setup_log()

        self.logger = logging.getLogger(__name__)
        self.logger.debug("Debug msg")
        self.logger.info("Info msg")
        self.logger.warning("Warn msg")  

        # Create TDM specific objects, the tasks built from .json files
        # and the Meaning extractor (MEx).
        self.MEx    = MEx.MEx()
        self.YTTM   = YTTM_talk.YTTM_talk()
        self.Nuance = Nuance.Nuance()
        self.Tasks  = TaskHandler.TaskHandler(self.Nuance)


    def start_at(self, json_name):
        """
        Run an instance of the tdm starting from the named json file
        """


    def check_for_person(self):
        """
        Monitors if there is a person in the vicinity, if there is
        """
        # TODO Add this functionality
        return True


# Psyclone cranc definition


# Debug function
if __name__ == "__main__":
    obj = TDM()
    # Test nuance output, send line for interpretation
    obj.start_at("greet")
    time.sleep(1)
    print "Debugging TDM finished"
    print 10*'*'
    print "Debug log output: "
    print 10*'*'
    os.system("cat Logging/*.log")
