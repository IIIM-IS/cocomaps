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
import logging
from timeit import default_timer as timer


def PsyCrank(apilink):
    api = cmsdk2.PsyAPI.fromPython(apilink)
    name = api.getModuleName()

    # Initialize TDM to be used for the system
    _TDM = TDM.TDM()
    logger = logging.getLogger("TDM_psyclone")
    # Definition of used variables
    I_CAN_SPEAK = True
    I_TALK_TO_PERSON = True
    check_who_is_speaking = True
    out_speak_buffer = None
    last_speak_time = 0
    while api.shouldContinue():
        msg = api.waitForNewMessage(150)

        if msg:
            trigger_name = api.getCurrentTriggerName()
            logger.debug("#TDM: Trigger name : {}".format(
                trigger_name))

            if trigger_name == "OtherIsSpeaking" and check_who_is_speaking:
                I_TALK_TO_PERSON = False
                check_who_is_speaking = False
            elif trigger_name == "Ready":
                api_trigger("Ready", api)
                _TDM.set_system_id(api.getParameterInt("SystemID"))
            elif trigger_name == "DialogOn":
                api_trigger("DialogOn", api)
                logger.debug("TMD: Turning on")
                _TDM.turn_on()
            elif trigger_name == "DialogOff":
                api_trigger("DialogOff", api)
                logger.debug("Turning off")
                _TDM.turn_off()

            if _TDM.is_active() and I_TALK_TO_PERSON:
                if check_who_is_speaking:
                    check_who_is_speaking = False
                    api.postOutputMessage("IAmSpeaking")
                # Debugging in psyclone
                check_speech_stack = _TDM.speak_stack.print_stack()
                api.setPrivateData("SpeachStack",
                                   check_speech_stack,
                                   len(check_speech_stack),
                                   "text/text")

                if _TDM.current_task is not None:
                    out_str =str(_TDM.current_task.name)
                    api.setPrivateData("TDM_current_task",
                                       out_str,
                                       len(out_str),
                                       "text/text")
                else:
                    out_str = "No task active"
                    api.setPrivateData("TDM_current_task",
                                       out_str,
                                       len(out_str),
                                       "text/text")

                if trigger_name == "NewWords":
                    api_trigger("NewWords", api)
                    if _TDM.word_bag_enabled:
                        _TDM.add_to_word_bag(msg.getString("Utterance"))
                elif trigger_name == "RobotSpeakingStarted":
                    api_trigger("RobotStartedSpeaking", api)
                    _TDM.robot_start_speaking(msg.getInt("CurrentSpeaker"))
                elif trigger_name == "RobotSpeakingStopped":
                    api_trigger("RobotStoppedSpeaking", api)
                    _TDM.robot_start_speaking(msg.getInt("CurrentSpeaker"))
                    _TDM.robot_stopped_speaking(msg.getInt("CurrentSpeaker"))

                # Flags set if the input type is speak
                if trigger_name == "Speak":
                    I_CAN_SPEAK = True
                elif trigger_name == "NoSpeak":
                    I_CAN_SPEAK = False

                # Need to have actions on a special branch
                if trigger_name == "TaskAccepted":
                    api_trigger("TaskAccepted", api)
                    # TODO implement in system.
                    pass
                elif trigger_name == "TaskCompleted":
                    taskID = msg.getInt("ReferenceID")
                    logger.debug( "#TDM: Task completed, task id {} type: {}".format(
                        taskID,
                        msg.getInt("Type")))

                    api_trigger("TaskCompleted", api)
                    _TDM.active_actions.add_finished_id(taskID)
                    if msg.getInt("Type") == 2:
                        # Type 1 == Panel control return
                        screen_name = msg.getString("ScreenName")
                        logger.debug("#TDM: psyclone screen name: {}".format(
                            screen_name))

                        if (_TDM.current_task.name in ["PanelA", "PanelB"]
                            and screen_name is not None):
                            # At top level the panel object is stored in the
                            # storage part of the task, PanleAA
                            current_panel_obj = _TDM.get_storage()
                            current_panel_obj.update(screen_name)
                        elif _TDM.get_storage() and screen_name is not None:
                            # Inside the menu, we store the task PanelA and
                            # are running a different window. So, assuming
                            # that the window does change
                            _TDM.set_window_by_reference(screen_name)
                            out_str = "Setting window to {}".format(
                                screen_name)
                            api.setPrivateData("Panel",
                                               out_str,
                                               len(out_str),
                                               "text/text")
                            out_str = "{}".format(screen_name)
                            api.setPrivateData("TDM_Panel",
                                               out_str,
                                               len(out_str),
                                               "text/text")
                    # Check if the return value was pin code, if pincode check
                    # if the value failed or succeeded
                    elif msg.getInt("Type") == 101:
                        status = msg.getString("Status")
                        logger.debug("#TDM : status: {}".format(status))
                        if status == "Failed":
                            _TDM.return_fail()
                        elif status == "Success":
                            _TDM.return_pass()
                        elif trigger_name == "TaskTimeout":
                            _TDM.return_fail()
# # # # # # Each run, if active, even if no msg is found run silent
        if _TDM.is_active():
            _TDM.silent_run()
            # Print to psyclone
            out_Str = _TDM.active_actions.print_stack()
            api.setPrivateData("Active_Actions",
                               out_Str,
                               len(out_Str),
                               "text/text")

            out_Str = _TDM.action_stack.print_stack()
            api.setPrivateData("Action Stack",
                               out_Str,
                               len(out_Str),
                               "text/text")

            # Check if there are any actions on the stack
            data = _TDM.check_action_stack()

            # Check if TDM has thrown go_to_search
            if _TDM.go_to_search == "True":
                data = None
                _TDM.reset()
                check_who_is_speaking = True
                I_CAN_SPEAK = False
                api.postOutputMessage("Talk",
                                      createAudioFromText(
                                          "Going into search mode"
                                      ))

                api.postOutputMessage("GoIntoSearchMode")

            # If the system is still active, start examening the outputs
            # outputs type are objects that are related to active stacks
            if hasattr(data, "type"):

                if data.type == "move":
                    msg1, msg2 = createMoveObject(data)
                    msg1.setInt("ReferenceID", data.id())
                    api.postOutputMessage("PerformTask", msg1)
                    api.postOutputMessage("Talk", createAudioFromText(msg2))
                    logger.debug("#TDM move id : {}".format(data.id()))
                    # Screen handling
                if data.type == "screen_msg":
                    msg = createScreenMsg()
                    out_str = "Screen type :{}".format(data.msg)
                    api.setPrivateData("Screen_type",
                                       out_str,
                                       len(out_str),
                                       "text/text")

                    logger.debug("#TDM starting {}".format(data.msg))
                    # Screen handling subtypes.
                    if data.msg == "Reset":
                        # Let psyclone know what is happening
                        out_str = "Sending reset msg"
                        api.setPrivateData("Panel",
                                           out_str,
                                           len(out_str),
                                           "text/text")

                        # Write to task executor
                        msg.setString("Name", "ResetScreen")
                    elif data.msg == "Query":
                        # Let psyclone knwo what is happening
                        out_str = "Sending query msg"
                        api.setPrivateData("Panel",
                                           out_str,
                                           len(out_str),
                                           "text/text")

                        # Write to task executor
                        msg.setString("Name", "ReadScreen")
                    elif data.msg == "BackButton":
                        out_str = "Pressing back button"
                        api.setPrivateData("Panel",
                                           out_str,
                                           len(out_str),
                                           "text/text")

                        msg.setString("Name", "NavigateBack")
                    elif data.msg == "Pin":
                        out_str = "Processing pin : {}".format(
                            data.push_button)
                        api.setPrivateData("Panel", out_str,
                                           len(out_str),
                                           "text/text")

                        msg.setString("pin", str(data.push_button))
                        msg.setInt("Type", 101)
                        # Robot responds == speech,
                        # Robot stays silent != speech
                        # msg.setString("Name", "EnterScreenPinSpeach")
                        msg.setString("Name", "EnterScreenPin")
                    elif data.msg == "PushButton":
                        str_out = data.push_button
                        out_str = "Pushing button - {}".format(str_out)
                        api.setPrivateData("PushButton", out_str, len(out_str),
                                           "text/text")
                        msg = createPushButton()
                        msg.setString("SelectScreenOption", str_out)
                        msg.setString("OptionName", data.get_button_to_push())
                    # Send the msg created
                    msg.setInt("ReferenceID", data.id())
                    logger.debug("#TDM:PSYCLONE: REF id: {}, {}".format(
                        msg.getInt("ReferenceID"),
                        msg.getString("Name")))
                    if data.msg == "Pin":
                        logger.debug("#TDM:PSYCLONE pin: {}".format(
                            msg.getString("pin")))

                    api.postOutputMessage("PerformTask", msg)

              # Add a better logic have a flag that is turned on off
            if I_CAN_SPEAK:
                data = _TDM.get_speak_stack()
                if data is not None:
                    I_CAN_SPEAK, out_speak_buffer, last_speak_time = TDM_speak(
                                                    api,
                                                    data.msg,
                                                    I_CAN_SPEAK,
                                                    out_speak_buffer,
                                                    last_speak_time)


# TODO - Add functionality:
# - Check if input is repeated, if so say something else
# - Give output time delay so we don't speak over itsel
def TDM_speak(api, msg, I_CAN_SPEAK, out_speak_buffer, last_speak_time):
    # SET beta here
    if timer() - last_speak_time > 3:  # beta
        if out_speak_buffer is not None:
            if (msg == out_speak_buffer and msg != "Could you please repeat that"):
                msg = "Could you please repeat that"
            elif (msg == out_speak_buffer and msg == "Could you please repeat that"):
                msg = " "
        out_speak_buffer = msg
        api.postOutputMessage("Talk", createAudioFromText(msg))
        last_speak_time = timer()
        I_CAN_SPEAK = False
        return I_CAN_SPEAK, out_speak_buffer, last_speak_time
    return I_CAN_SPEAK, out_speak_buffer, last_speak_time


def createAudioFromText(inString):
    """
    Create a psyclone project specific output string to send to
    the audio interpretor
    """
    inString = str(inString)
    msg = cmsdk2.DataMessage()
    msg.setString("Utterance", inString)
    msg.setInt("Type", 0)

    return msg


def createMoveObject(move_type):
    """
    Rip information from the move type object that is passed in.
    The object contains the name of the expected point
    """
    # TODO, fix this to represent the actual data message
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "NavigateToNamedPointSpeech")
    # msg.setString("Name", "NavigateToNamedPoint")
    msg.setString("Role", "Controller")
    msg.setInt("Timeout", 30000)
    msg.setString("PointName", str(move_type.point))
    msgStr = move_type.msg

    return msg, msgStr


def createScreenMsg():
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "PanelControl")
    msg.setString("Role", "Controller")
    # Comment out below to use in real, use below for debug
    # msg.setString("Role", "Communicator")
    msg.setInt("Timeout", 5000)
    msg.setInt("Type", 2)

    return msg


def createPushButton():
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "SelectScreenOption")
    msg.setString("Role", "Controller")
    msg.setInt("Timeout", 5000)
    msg.setInt("Type", 3)
    return msg


def api_trigger(msg, api):
    api.setPrivateData("TDM_trigger", msg, len(msg), "text/text")


if __name__ == "__main__":
    obj = TDM.TDM()
    print obj.word_bag.printall()
