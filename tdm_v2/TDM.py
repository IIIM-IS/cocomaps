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


# Custom modules
from MEx import MEx
from TaskBuilder import TaskBuilder


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

        logger = logging.getLogger(__name__)
        logger.debug("Debug msg")
        logger.info("Info msg")
        logger.warning("Warn msg")  

        # Create TDM specific objects, the tasks built from .json files
        # and the Meaning extractor (MEx).
        self.Tasks  = TaskBuilder.TaskBuilder()
        self.MEx    = MEx.MEx()


# Psyclone cranc definition


# Debug function
if __name__ == "__main__":
    obj = TDM()

