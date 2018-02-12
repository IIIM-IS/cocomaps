#! /usr/bin/env python
#################################################################################
#     File Name           :     tdm_raw.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-12 15:24]
#     Last Modified       :     [2018-02-12 15:53]
#     Description         :     A raw version for simple debug. Uses MEx to
#                                   map keywords to specific output text, values
#     Version             :     1.0
#################################################################################

import cmsdk2
from MEx import MEx


def PsyCrank(apilink=None):
    # For debugging offline
    if apilink != "debug":
        api = cmsdk2.PsyAPI.fromPython(apilink)

    tdm = tdm_raw()

    tests = ["This sentence comes first", "This sentence comes second",
            "Say hello to me robot"]

    # if message is set to read
    for input_msg in tests:
        tdm.add_message(input_msg)
    tdm.search()



class tdm_raw(object):
    """
    Storage container for information
    """
    def __init__(self):
        self.word_buffer = []
        self.MEx = MEx.MEx()
        self.search_fields = ["hello", "move", "point1", "point2"]

    def search(self):
        """
        Search the newest input for value types
        """
        words = []
        for sentence in self.word_buffer:
            for word in sentence:
                words.append(word)
        print words


    def add_message(self, input_msg):
        """
        Adds inputs from Nuance when ready
        """
        if len(self.word_buffer) > 20:
            self.word_buffer.insert(0,input_msg.split(" "))
            self.word_buffer.pop()
        else:
            self.word_buffer.insert(0,input_msg.split(" "))



if __name__ == "__main__":
    print "Running main for tdm_raw"
    PsyCrank("debug")
    print "Finished running main"


