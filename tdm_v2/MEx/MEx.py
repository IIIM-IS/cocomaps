#!/usr/bin/python2.7
"""
24.01.18
Author
    david@iiim.is

About
    The meaning extractor takes in a sentance or a set of words and tries to 
    map them to specific output responses. 
"""

import logging
from threading import Thread


class MEx(Thread):
    """
    Meaning extractor object, called in the beginning of the tdm and stored
    in background. Uses various specially constructed dictionaries
    """
    def __init__(self):
        Thread.__init__(self)
        self.daemon = False
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Starting up MEx")

        self.DB = self.create_word_association_database()


    def create_word_association_database(self):

        """
        Built in method for reading a datastructure and mapping words
        to other words and meanings
        """
        self.logger.info("Creating MEx database")
        DB = None

        return DB

    def eval(self, words, keys):
        """
        Evaluate words, assume words are sentances, and try to use the 
        MEx database to map those words to the keys(meanings)
        """
        self.logger.debug("Processing words/keys:\n\t\t{}\n\t\t{}".format(words,
                                                                       keys))
        pass

# todo, create word association databank using json. E.g. phone, call, ring, 
# are all connected; create chains of words that return increased values 
# for "parent" concept. 
