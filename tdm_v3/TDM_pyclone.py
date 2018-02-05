#!/usr/bin/python2.7
"""
02.01.18
Author
    David Orn : david@iiim.is
About
    This file contains the actual psyclone to TDM connector
    to be run during operations. 
    Development reasons are to figure out how best to operate
    the system and what functions are needed, finally what
    action structure is most relevant
"""
__author__ = "David"
from CMSDK_lib import cmsdk2.py
import TDM

def PsyCrank(apilink):
    api = cmsdk2.PsyAPI.fromPython(apilink)
    name = api.getModuleName()

    # Initialize TDM to be used for the system
    _TDM = TDM.TDM()

    while api.shouldContinue():
        msg = api.waitForNewMessage(50)

        # Update relevant information
        _TDM.initialize()
        
