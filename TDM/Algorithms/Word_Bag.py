#! /usr/bin/env python
#################################################################################
#     File Name           :     Word_Bag.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-26 12:39]
#     Last Modified       :     [2018-02-26 17:10]
#     Description         :     Store input values when available try to 
#                               use them when available
#     Version             :     0.1
#################################################################################

from timeit import default_timer as timer
import logging
import re

class Word_Bag(object):
    """
    Store the input words for a while. Clear buffer when called or within 
    a certain limit of time
    """
    def __init__(self):
        """
        Initialize an empty set of words
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Started up Word_Bag")
        self.name = "Word Bag"
        self.init_time = timer()
        self.newest_words = 0

        self.len = 0

        self.new_words = False
        self.buffer = []

    def add(self, input):
        """
        Add new set of words to bag, split words into variables and
        set flags where appropriate
        """
        self.new_words = timer()
        if input != "":
            re.sub('[^A-Za-Z0-9]+', '', input)
            input = input.split(" ")
            if self.buffer:
                self.buffer.insert(0, input)
            else:
                self.buffer = input
            self.new_words = True

    def clean(self):
        """
        Clear the buffer input. Store for debugging purposes
        """
        self.logger.info("Cleaning bag:")
        for sentence in self.buffer:
            self.logger.info("\t{}".format(sentence))
        self.buffer = []
        self.new_words = False


    def get(self):
        """
        Get the newest set of input words
        """
        if self.elapsed():
            self.new_words = False
            self.clean()
    
        if self.buffer and self.new_words:
            self.new_words = False
            return self.buffer
        else: 
            return False

    def elapsed(self):
        """
        Check if long time since last input was recieved
        """
        if timer() - self.newest_words > 60:
            return False
        return True

