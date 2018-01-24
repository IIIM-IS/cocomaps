#!/usr/bin/python2.7
"""
Author 
    david@iiim.is

About:
    This file contains a simple helping function for determining the file
    name of the output log file to be created. Assumes it is called from 
    the tdm_v2/ directory (one above current directory, since the tdm will
    call it)
"""
import datetime, os, logging

def log_name():
    """
    Create a name for the log file, return a string
    """
    here = os.getcwd();
    now = datetime.datetime.now().strftime("%m-%dT%H:%M:%S")
    outStr = here + "/Logging/" + now + ".log"
    return  outStr


def setup_log():
    """
    Setting up logging definition for the logger
    """
    logging.basicConfig(filename=log_name(),
                       format = "%(asctime)s;%(name)3s;%(message)s",
                       level=logging.DEBUG)
