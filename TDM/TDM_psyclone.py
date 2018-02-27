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
import cmsdk2 
import TDM

print "This is a test"

def PsyCrank(apilink):
    api = cmsdk2.PsyAPI.fromPython(apilink)
    name = api.getModuleName()

    # Initialize TDM to be used for the system
    print "This is going"
    _TDM = TDM.TDM()

    while api.shouldContinue():
        msg = api.waitForNewMessage(200)

        if msg:
            trigger_name = cmsdk2.getCurrentTriggerName()

            if trigger_name == "NewWords":
                _TDM.add_message(msg.getString("Utterance"))

            elif trigger_name == "MyTurn":
                # Do something to check that it's my turn 
                internal_msg = _TDM.run()
                
                # Output speech comes through here
                if internal_msg["Result"] == "out_msg":
                    api.postOutputMessage("Utterance", internal_msg["Text"])

                elif internal_msg["Result"] == "Location":
                    api.postOutputMessage("Location", internal_msg["Location"])

                else :
                    print "trigger name: {}".format(trigger_name)
            api.postOutputMessage("RobotGivesTurn", 1)



        else:
            print "Nothing to report"
