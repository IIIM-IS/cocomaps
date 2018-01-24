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


# DEBUG : CLEAN LOGGING FOLDER
os.system("find Logging/ -name *.log -exec rm {} \;")
# Setup the logging module for getting, setting and storing information
import logging
from Logging.tdmLogging import setup_log
setup_log()

logger = logging.getLogger(__name__)
logger.debug("Debug msg")
logger.info("Info msg")
logger.warning("Warn msg")


# Build task definitions
tasks = TaskBuilder.TaskBuilder()

# Try making a MEx object
_MEx = MEx.MEx()

