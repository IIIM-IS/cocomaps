#! /usr/bin/env python
#################################################################################
#     File Name           :     tdm_raw.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-12 17:18]
#     Last Modified       :     [2018-02-12 17:39]
#     Description         :     Interface object. Stores information 
#                                and returns message outputs in psyclone form
#     Version             :     1.0
#################################################################################
# Import from python space
import logging

# Object specific imports
from MEx import MEx
import tdm_logger as log_setup
import cmsdk2


class tdm_raw(object):
    """
    ...
    """
    def __init__(self):
        # Setup logging according to file
        log_setup.setup_logging()
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Starting TDM object")
        self.MEx = MEx.MEx()
        self.word_buffer = []

        # Define types that can be searched, in final product this method
        # is defined in json files.
        self.types = ["hello", "move", 
                      "point1", "point2"]

    def input_words(self, words):
        # Split working input into
        # array
        words = words.lower().split(" ")
        if len(self.word_buffer) > 10:
            self.word_buffer.insert(0,words)
            self.word_buffer.pop()
        else :
            self.word_buffer.insert(0,1)

    def run(self):
        """
        Wait for my turn for the robot
        to start the return value, whatever it
        is
        """
        p = self.MEx.dict_search(self.types,
                                self.word_buffer)



if  __name__ == "__main__":
    print "Offline debug mode"
    obj = tdm_raw()
    t_sentences = ["Say hello", "Move to point one", "move to point two"]
    for sentence in t_sentences:
        obj.input_words(sentence)

    print 20*'*'
    print "\t\t Debug finished"
    print 20*'*'
