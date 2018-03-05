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
from TDM import TDM

from timeit import default_timer as timer

def PsyCrank(apilink):
    api = cmsdk2.PsyAPI.fromPython(apilink)
    name = api.getModuleName()

    # Initialize TDM to be used for the system
    _TDM = TDM.TDM()
    count = 0

    while api.shouldContinue():
        msg = api.waitForNewMessage(200)
        if msg:
            trigger_name = api.getCurrentTriggerName()
            print "TRIGGER INPUT: {}".format(trigger_name)

            if trigger_name == "NewWords":
                _TDM.add_words(msg.getString("Utterance"))

            elif trigger_name == "MyTurn":
                internal_msg = _TDM.run()

                if "Result" in internal_msg.keys():
                    if internal_msg["Result"] == "Talk":
                        # Wait for the system to give a go ahead for talking
                        start = timer()
                        while not _TDM.can_talk():
                            if timer() - start > 3:
                                print "Something went wrong in waiting for timeslot"
                                break
                        api.postOutputMessage("Talk", createAudioFromText(
                                                        internal_msg["msg"]))
                        _TDM.talk_delay(internal_msg["msg"])

                    elif internal_msg["Result"] == "Move":
                        msg, msgString = createMoveObject(internal_msg["Point"])

                        # Post the move command
                        api.postOutputMessage("PerformTask", msg)
                        # Let the user know
                        api.postOutputMessage("Talk", createAudioFromText(
                                                    msgString
                        ))
                        _TDM.talk_delay(msgString)


        else:
            None
            # Could implement silent run in the future. Now everything
            # is online


def createAudioFromText(inString):
    """
    Create a psyclone project specific output string to send to 
    the audio interpretor
    """
    inString = str(inString)
    print "Debugging: instr type: {}, value: {}".format(type(inString), inString)
    msg = cmsdk2.DataMessage()
    msg.setString("Utterance", inString)
    
    return msg


def createMoveObject(int_msg):
    """
    Create a psyclone message interpolating the data needed to send
    the executor to a location on the map
    """
    # TODO, fix this to represent the actual data message
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "NavigateToNamedPoint")
    msg.setString("Role", "Controller")
    msg.setInt("Timeout", 30000)
    

    if int_msg == "Point1":
        msg.setString("PointName", "ControlPanel1")
        msgStr = "Sending controller to point 1"


    elif int_msg == "Point2":
        msg.setString("PointName", "ControlPanel2")
        msgStr = "Sending controller to point 2"

    return msg, msgStr

