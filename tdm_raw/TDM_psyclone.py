#! /usr/bin/env python
#################################################################################
#     File Name           :     tdm_raw.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-12 17:13]
#     Last Modified       :     [2018-02-14 10:01]
#     Description         :     A shorter verion of the TDM used for unofficial
#                               demo 2
#     Version             :     1.0
#################################################################################

import cmsdk2
from MEx import MEx
from tdm_raw import tdm_raw

def PsyCrank(apilink):
    api = cmsdk2.PsyAPI.fromPython(apilink)

    tdm_obj = tdm_raw()

    while api.shouldContinue():
        msg = api.waitForNewMessage(50)

        if msg:
            trigger_name = msg.getCurrentTriggerName()
            if trigger_name == "NewWords":
                # Read values from Nunace and store
                # in tdm until it's tdm's time to
                # answer
                words = msg.getString("Utterance")
                tdm_obj.input_words(words)
            elif trigger_name == "MyTurn":
                res_msg = tdm_obj.run()
                if res_msg["Result"] == "OutMSg":
                    api.postOutputMessage("Utterance", res_msg["Text"])
                elif res_msg["Result"] == "move":
                    # Send message for robot to move
                    # currently no response or timeout
                    if res_msg["Point"] == "A":
                        api.postOutputMessage("perform_task", res_msg["msg"])
                        api.postOutputMessage("Utterance", res_msg["Text"])
                    elif res_msg["Point"] == "B":
                        api.postOutputMessage("perform_task", res_msg["msg"])
                        api.postOutputMessage("Utterance", res_msg["Text"])
                    elif res_msg["Point"] == "C":
                        api.postOutputMessage("perform_task", res_msg["msg"])
                        api.postOutputMessage("Utterance", res_msg["Text"])


