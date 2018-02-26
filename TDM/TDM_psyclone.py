#! /usr/bin/env python
#################################################################################
#     File Name           :     tdm_raw.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-12 17:13]
#     Last Modified       :     [2018-02-26 15:09]
#     Description         :     A shorter verion of the TDM used for unofficial
#                               demo 2
#     Version             :     1.0
#################################################################################

import cmsdk2
import TDM

def PsyCrank(apilink):
    api = cmsdk2.PsyAPI.fromPython(apilink)
    _TDM = TDM.TDM()

    # Print version notes
    _TDM.version_notes()

    while api.shouldContinue():
        msg = api.waitForNewMessage(50)

        if msg:
            trigger_name = msg.getCurrentTriggerName()
            if trigger_name == "NewWords":
                # Read values from Nunace and store
                # in tdm until it's tdm's time to
                # answer
                _TDM.input_text(msg.getString("Utterance"))
            elif trigger_name == "MyTurn":
                res_msg = _TDM.run()
                if res_msg["Result"] == "out_msg":
                    api.postOutputMessage("Utterance", res_msg["Text"])
                elif res_msg["Result"] == "move":
                    api.postOutputMessage("Move", res_msg["Location"])

