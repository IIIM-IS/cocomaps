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
import json
import numpy as np


class MEx(Thread):
    """
    Meaning extractor object, called in the beginning of the tdm and stored
    in background. Uses various specially constructed dictionaries
    """
    def __init__(self, api=None):
        Thread.__init__(self)
        self.daemon = False
        self.logger = logging.getLogger(__name__)
        self.name_db = Person()
        self.logger.debug("Starting up MEx")

        self.create_word_association_database()

        # Regarding psyclone or other conections
        self.api = api


    def create_word_association_database(self):

        """
        Built in method for reading a datastructure and mapping words
        to other words and meanings
        """
        self.logger.info("Creating MEx database")
        
        print __file__
        curr_loc = __file__[:-7]
        file_name = curr_loc+"/word_association_db.json"
        with open(file_name, "rb") as fid:
            DB = json.loads(fid.read())

        self.logger.debug("Created database")
        for key in DB.keys():
            self.logger.debug("\t{}".format(key))
            for value in DB[key]:
                self.logger.debug("\t\t{} - {}".format(value, DB[key][value]))

        self.DB = DB

    def eval_backend(self, words, input_keys):
        """
        Backend of word evaluation, computed after searching for possible
        persons and or abort sequences in the sentance.
        Processing method, assume words are sentances, and try to use the 
        MEx database to map those words to the keys(meanings) and compute
        probability of sentance
        """
        self.logger.debug("Processing words/keys:\n\t\t{}\n\t\t{}".format(words,
                                                                    input_keys))

        p_out = np.zeros(len(input_keys))
        # Compare each key to the word in the sentace, return the probability
        # that the key is connected to the word
        for idx, key in enumerate(input_keys):
            self.logger.debug("Processing key: {}".format(key))
            for word in words:
                if word in self.DB[key].keys():
                    self.logger.debug("\t\tAdding value with: '{}'".format(word))
                    p_out[idx] += self.DB[key][word]

        # Normalize the output
        p_out = p_out/(len(words)*100)  #100 because items are stored in range
                                        # 0-100

        return p_out

    def eval(self, words, input_keys):
        """
        First search for possible humans by using the person detector, then 
        search for possible abort sentances, if abort sentances set misc output
        to reason and follow up
        """

        # Check for abort
        p = self.eval_backend(words, ["abort"])
        if p > .5:
            return None, None, True
        else :
            persons = []
            ID = []
            for word in words:
                person, _id= self.Person.search(word)
                if person:
                    if person and _id not in ID:
                        persons.append(person)
                        ID.append(_id)
                    
            return self.eval_backend(words, input_keys), persons, False


class Person(object):
    """
    Object class for persons, a person contains information regarding
    who the person is and a search method to check if a word can be 
    assumed to be a name
    """
    def __init__(self):
        """
        Initialize the person database by reading the personel file, 
        persons.json in the same folder
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info("Loading personel database")
        
        print __file__
        curr_loc = __file__[:-7]
        file_name = curr_loc+"/personel_db.json"
        with open(file_name, "rb") as fid:
            self.DB = json.loads(fid.read())

        self.names = []
        # Names are stored in list of list
        # e.g.
        # self.names =  [[Thor, List]
        #                [""]
        self.names = []
        for val in self.DB:
            self.names.append([self.DB[val]["name"].lower().split(), val])
        self.logger.debug("Personel files loaded")


    def search(self, word):
        for value in self.names:
            name = value[0]
            if word in name:
                return self.DB[value[1]], value[1]
        return None, None
            
# todo, create word association databank using json. E.g. phone, call, ring, 
# are all connected; create chains of words that return increased values 
# for "parent" concept. 
