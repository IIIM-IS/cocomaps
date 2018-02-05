#!/usr/bin/python2.7
"""
01.02.18
Author
    david@iiim.is

About
    The meaning extractor takes in a sentance or a set of words and tries to 
    map them to specific output responses. 
"""
__author__ = "david"
import json, os, logging, sys, numpy as np
from threading import Thread

from Types import Actions_def
from Types import Locations_def
from Types import Tasks_def

class MEx(Thread):
    """
    (M)eaning (Ex)tractor is built from current location by reading all possible
    types in folder Types, one directory up from current location
    """
    def __init__(self, api=None):
        Thread.__init__(self)

        # Start a logging object
        self.logger = logging.getLogger(__name__)
        self.logger.info("MEx starting up")
        self.logger.debug("MEx started up")
        
        temp = os.getcwd()
        char_loc = temp.find("tdm_v3")+6
        print char_loc
        self.MasterLocation = temp[:char_loc] + '/MEx/'
        print self.MasterLocation
        
        # Read in Types used in project
        self.Types = {}
        with open(self.MasterLocation+"MEx.init", 'rb') as fid:
            for line in fid:
                clean_line = line.rstrip()
                self.Types[clean_line] = {}
        
        # Having aquired which objects will be used in the system we can
        # load all possible objects and create a dictionary
        self.create_objects()

        # If there is an available API input then input specific api
        if api:
            self.api = api


        self.logger.info("MEx initialized without errors")
        self.logger.debug("MEx initialized without errors")

    def create_objects(self):
        """
        Create a dictionary based on the file structure. Read each json file 
        and connect each type to a word
        """
        for _type in self.Types:
            location = self.MasterLocation+"Types/"+_type
            sys.path.append(location)
            curr_decoder = get_object_decoder(_type)
            self.logger.debug("Adding _type {}".format(_type))
            for json_file in os.listdir(location):
                if os.path.splitext(json_file)[1]==".json":
                    temp_obj = None
                    self.logger.debug("Decoding file: {}".format(json_file))
                    with open(location+"/"+json_file, 'rb') as fid:
                        text = fid.read()
                        self.logger.debug("{}".format(text))
                        if text:
                            temp_json = json.loads(text)
                            temp_obj  = curr_decoder(temp_json)
                            
                    if temp_obj:
                        self.logger.debug("{} \n {}".format(temp_obj, type(temp_obj)))
                        self.logger.debug("Adding type:{} with name: {}".format(
                                _type, temp_obj.name
                        ))
                        self.Types[_type][temp_obj.name] = temp_obj
    
    def dict_search(self, _type, search_keys, W):
        self.logger.debug("Processing words: '{}' ; with _type:{} ; search_keys:{}".format(
                                                                W, _type, search_keys))
        p = np.zeros(len(search_keys))
        for word in W:
            self.logger.debug("Word: {}".format(word))
            for idx, key in enumerate(search_keys):
                if word in self.Types[_type][key].dictionary:
                   p[idx] += p[idx] + \
                        float(self.Types[_type][key].dictionary[word])/100
        self.logger.info("P values for words {}".format(p))
        return p/len(W)

def get_object_decoder(_type):
    if _type == "Actions":
        return Actions_def._Type.obj_decoder
    elif _type == "Tasks":
        return Tasks_def._Type.obj_decoder
    elif _type == "Locations":
        return  Locations_def._Type.obj_decoder
    else :
        return None

# Debugging method
if __name__ == "__main__":
    from tdm_logger import setup_logging
    setup_logging()
    obj = MEx()
    sentenses = ["Could you tell me a joke",
                "Please start up generator three",
                "Answer me this question"]
    keywords =  ["start_generator", "ask_question", "tell_joke"]
    for sent in sentenses:
        obj.logger.debug(sent)
        p=obj.dict_search("Tasks",keywords, sent.lower().split())

        print keywords[np.argmax(p)]






