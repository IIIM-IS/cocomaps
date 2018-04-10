#! /usr/bin/env python
#################################################################################
#     File Name           :     MEx.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2017-11-14 17:58]
#     Last Modified       :     [2018-03-27 09:39]
#     Description         :     (M)eaning (Ex)tractor for the cocomaps project
#                               between IIIM and CMLabs. 
#                               Creates a dictionary using keyword search.
#     Version             :     3.1
#################################################################################

import logging
import numpy as np



class MEx(object):
    """
    Top object storer. Creates and stores all types, reads in the dictionary 
    and computes word connections. 
    """
    def __init__(self, tasks):
        """
        Create the dictionary set fom the information stored in the
        tasks types
        """
        self.logger = logging.getLogger(__name__)
        self.dict = {}
        for key in tasks.Tasks.keys():
            for _type in tasks.Tasks[key].keywords:
                words = []
                for word in tasks.Tasks[key].keywords[_type]: 
                    words.append(word)
                if _type in self.dict.keys(): 
                    for instance in self.dict[_type]:
                        if instance not in words and instance != "":
                            words.append(instance)

                self.dict[_type] = words

        self.print_available()

    def dict_search(self, keywords, word_bag):
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
        self.logger.debug("#TDM: Searcing sentence {}. With keywords {}".format(
                            word_bag.get(),
                            keywords
        ))

        p = np.zeros(len(keywords))

        
        for i in range(word_bag.len):
            alpha = 1.0/(1.0 - np.exp(-(i+1)))
            for word in word_bag.get(no=i):
                self.logger.debug("#TDM: {}/{} : {}".format(i, alpha, word))
                for idx, key in enumerate(keywords):
                    # Assumptions, keywords must have dictionary definitions
                    # or this breaks
                    if self.is_in_dict(word, self.dict[key]):
                        self.logger.debug("#TDM: word: {}".format(word))
                        p[idx] += 1*alpha

        self.logger.debug("#TDM: Results are {}".format(p))
        return p

    def pin_search(self, word_bag):
        """
        Search for number values in the word bag. Specifically a 4 
        number value that comes in in sequence.
        """

        pin_length = 4

        for i in range(word_bag.len): # i = sentence id
            for word in word_bag.get(no=i):
                if len(word) == pin_length and word.isdigit():
                            return True, word
        return False, []

    def is_in_dict(self, word, keys):
        for key in keys:
            if key == word:
                return True
        return False


    def print_available(self):
        """
        Print available types within currently loaded structure
        """
        
        print "Available objects in current structure \n"
        for _type in self.dict.keys():
            print "Type: {}".format(_type)
            for object in self.dict[_type]:
                print "\t\t{}".format(object)


if __name__=="__main__":
    pass
