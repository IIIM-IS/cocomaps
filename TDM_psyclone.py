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
__author__ = "David Orn Johannesson"
import cmsdk2
from TDM import TDM

from timeit import default_timer as timer

def PsyCrank(apilink):
    api = cmsdk2.PsyAPI.fromPython(apilink)
    name = api.getModuleName()

    # Initialize TDM to be used for the system
    _TDM = TDM.TDM()

    while api.shouldContinue():
        msg = api.waitForNewMessage(150)

        if msg:
            trigger_name = api.getCurrentTriggerName()
            if trigger_name == "Ready":
                _TDM.turn_on()
            if _TDM.is_active():
                if trigger_name == "NewWords":
                    _TDM.add_to_word_bag(msg.getString("Utterance"))
                    # Remove later
                    _TDM.print_stat()

                elif trigger_name == "Speak":
                    data = _TDM.get_speak_stack()
                    if data != None:
                        api.postOutputMessage("Talk", createAudioFromText(data.msg))

                elif trigger_name == "TaskAccepted":
                    #TODO implement in system. 
                    pass
                                   
                elif trigger_name == "TaskCompleted":
                    taskID = msg.getInt("ReferenceID")
                    print "Triggered task complete, using refid {}".format(taskID)
                    _TDM.print_stat()
                    _TDM.active_actions.add_finished_id(taskID)
                    if msg.Type == "Panel":
                        if _TDM.current_panel_screen != None:
                            _TDM.current_panel_screen.update(msg.getString("ScreenName"))


                elif trigger_name == "TaskTimeout":
                    # TODO, add timoute functionality
                    # NOTE : There is a built in functionality in the TDM
                    pass

                elif trigger_name == "TaskCancelled":
                    # TODO : Add functionality to TDM. Can actually be the 
                    # same method as timeout, but with different name
                    pass

                #          PANEL CONTROL FUNCTION - not implemented
                # Update the information about the active panel message.
                elif trigger_name == "UpdatePanel":
                    if _TDM.current_panel_screen != None:
                        _TDM.current_panel_screen.update(msg)

        else:
            if _TDM.is_active():
                data = _TDM.check_action_stack()
                if hasattr(data, "type"):
                    if data.type == "move":
                        msg1, msg2 = createMoveObject(data)
                        msg1.setInt("ReferenceID", data.id())
                        api.postOutputMessage("Performtask", msg1)
                        api.postOutputMessage("Talk", createAudioFromText(msg2))
                    if data.type == "screen_msg":
                        if data.msg == "Reset":
                            pass
                            # Send the reset msg to the 
                        elif data.msg == "Query":
                            pass

                if _TDM.turn_dialog_off():
                    # TODO add this to XML file
                    # Currently a circular definition
                    _TDM.turn_off()
                    api.postOutputMessage("Talk", createAudioFromText(
                        "Going into search mode"
                    ))
                    api.postOutputMessage("DialogOff_1")
                _TDM.silent_run()

            """
            if data != None:
                if data.type == "move":
                    msg1, msg2 = createMoveObject(data)
                    api.postOutputMessage("Perform", msg1)
                    api.postOutputMessage("", createAudioFromText(msg2))

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
    """ Temporarily removed to test system
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "NavigateToNamedPoint")
    msg.setString("Role", "Controller")
    msg.setInt("Timeout", 30000)
    msg.setString("PointName", move_type.point)
    """
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "TestTask")
    msg.setString("Role", "Controller")
    msg.setInt("Timeout", 30000)
    msg.setInt("TestValue", 101)
    # Temporary


    msgStr = move_type.msg

    return msg, msgStr


if __name__ == "__main__":
    obj = TDM.TDM()
    print obj.word_bag.printall()
