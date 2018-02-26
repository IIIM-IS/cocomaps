#! /usr/bin/env python
#################################################################################
#     File Name           :     MEx.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2017-11-14 17:58]
#     Last Modified       :     [2018-02-26 13:57]
#     Description         :     (M)eaning (Ex)tractor for the cocomaps project
#                               between IIIM and CMLabs. 
#                               Creates a dictionary using keyword search.
#     Version             :     3.1
#################################################################################
import json
import os
import logging
import sys
import numpy as np



class MEx(object):
    """
    Top object storer. Creates and stores all types, reads in the dictionary 
    and computes word connections. 
    """
    def __init__(self):
        """
        Load dictionary from file, handle location issues.
        """
        # Start up a logger for monitoring and debugging reasons
        self.logger = logging.getLogger(__name__)
        self.logger.info("Creating MEx dictionary object")

        # Get the local path absolute extension
        self.curr = str(os.path.abspath(__file__))
        # There is an issue, somethimes an additional value (c) is added
        # to string. New method introduced to mitigate error
        loc = [pos for pos, char in enumerate(self.curr) if char=='/']
        self.curr = self.curr[:loc[-1]+1]
        # Create a dictionary file location variable
        dict_file = self.curr + "dictionary.json"

        # Create a holding place for the dictionary
        self._dict = {}
        # Load the dictionary
        self.make_dict(dict_file)

        self.logger.info("MEx has been built")


    def make_dict(self, dict_file):
        """
        Load a dictionary from a specific file, 
        input:
            dict_file : absolute string path to dictionary .json file
        output:
            appends a dictionary structure to the MEx class
        """
        self.logger.debug("Dict file: {}".format(dict_file))
        with open(dict_file, 'rb') as fid:

            raw_text = fid.read()
            raw_json = json.loads(raw_text)

        # Create dictionary structure
        for key in raw_json.keys():
            self.logger.debug("Adding key: {}".format(key))
            self.logger.debug("With values : {}".format(raw_json[key]))
            self._dict[key] = raw_json[key]


    def dict_search(self, _dict):
        """
        Only action types can search the dictionary. The actions have a 
        field named keywords that dictate which key within the dictionary
        is used to search for values

        inputs:
            _dict = Python dictionary with key attributes
                CurrentAction = action object currently searching for value
                * DEBUG
                Words = "Array of words split from sentense that user inputs"
        """
        #TODO : Add word buffer evaluation to the methodology. 
        action = _dict["CurrentAction"] 
        word_buffer = _dict["Words"]
        p = np.zeros(len(action.keywords))
        
        for idx,key in enumerate(action.keywords):
            for word in _dict["search_words"]:
                if key in self._dict.keys():
                    if word in self._dict[key].keys():
                        p[idx] += self._dict[key][word]


    def print_available(self):
        """
        Print available types within currently loaded structure
        """
        
        print "Available objects in current structure \n"
        for _type in self._dict.keys():
            print "Type: {}".format(_type)
            for object in self._dict[_type].keys():
                print "\t\t{}".format(object)


if __name__=="__main__":
    sys.path.append("..")
    import tdm_logger
    tdm_logger.setup_logging()
    obj = MEx()

