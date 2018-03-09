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

    while api.shouldContinue():
        msg = api.waitForNewMessage(100)

        if msg:
            trigger_name = api.getCurrentTriggerName()
            print "TRIGGER INPUT: {}".format(trigger_name)

            if trigger_name == "NewWords":
                _TDM.add_to_word_bag(msg.getString("Utterance"))

            elif trigger_name == "Speak":
                data = _TDM.check_speak_stack()
                if hasattr(data, "type"):
                    if data.type == "msg":
                        api.postOutputMessage("Talk", createAudioFromText(data.msg))

            # TODO Correct this with THOR
            elif trigger_name == "PerformTask":
                task_id = msg.getString("TaskID")
                status  = msg.getString("Status")


        else:
            data = _TDM.check_action_stack()
            
            if hasattr(data, "type"):
                if data.type == "move":
                    msg1, msg2 = createMoveObject(data)
                    api.postOutputMessage("Performtask", msg1)
                    api.postOutputMessage("Talk", createAudioFromText(msg2))
                    _TDM.add_timeout_by_string(msg2)
                    


            if _TDM.turn_dialog_off():
                # TODO add this to XML file
                api.postOutputMessage("DialogOff")



            """
            if data != None:
                if data.type == "move":
                    msg1, msg2 = createMoveObject(data)
                    api.postOutputMessage("Perform", msg1)
                    api.postOutputMessage("Talk", createAudioFromText(msg2))

                elif data.type == "screen_navigate"

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
            _TDM.silent_run()
            None
            # Could implement silent run in the future. Now everything
            # is online
            """


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


def createMoveObject(move_type):
    """
    Rip information from the move type object that is passed in. 
    The object contains the name of the expected point
    """
    # TODO, fix this to represent the actual data message
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "NavigateToNamedPoint")
    msg.setString("Role", "Controller")
    msg.setInt("Timeout", 30000)
    msg.setString("PointName", move_type.point)

    msgStr = move_type.msg

    return msg, msgStr
    
"""
    if int_msg == "Point1":
        msg.setString("PointName", "ControlPanel1")
        msgStr = "Sending controller to point 1"


    elif int_msg == "Point2":
        msg.setString("PointName", "ControlPanel2")
        msgStr = "Sending controller to point 2"
"""


if __name__ == "__main__":
    obj = TDM.TDM()
