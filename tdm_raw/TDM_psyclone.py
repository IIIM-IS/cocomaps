#! /usr/bin/env python
#################################################################################
#     File Name           :     tdm_raw.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-12 17:13]
#     Last Modified       :     [2018-02-12 17:35]
#     Description         :     A shorter verion of the TDM used for unofficial
#                               demo 2
#     Version             :     1.0
#################################################################################

import cmsdk2
from MEx import MEx
from tdm_raw import tdm_raw

def PsyCrank(apilink):
    if not apilink:
        api = cmsdk2.PsyAPI.fromPython(apilink)

    tdm_obj = tdm_raw()

    while api.shouldContinue():
        msg = api.waitForNewMessage(20)

        if msg:
            trigger_name = msg.getCurrentTriggerName()

            if trigger_name == "input_utterance":
                # Read values from Nunace and store
                # in tdm until it's tdm's time to
                # answer
                words = "This is a test"
                tdm_obj.input_words(words)
            elif trigger_name == "my_turn":
                # Return the relevant value
                # from inptu
                _dict = tdm_obj.run()

                




