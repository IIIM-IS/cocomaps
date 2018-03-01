#! /usr/bin/env python

#################################################################################
#     File Name           :     Objects.py
#     Created By          :     David Orn Johannesson
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-09 08:59]
#     Last Modified       :     [2018-03-01 13:55]
#     Description         :     An object holder for the different types
#                                   used inside TDM. Stores the values 
#                                   and defines type specific actions
#     Version             :     2.0
#################################################################################

import json
import os
import sys
import logging
import copy
from timeit import default_timer as timer
import numpy as np

# Import decoding methods
import Actions_def
import Tasks_def
import Locations_def


decoder = {
    "Tasks":Tasks_def._Type.obj_decoder,
    "Actions":Actions_def._Type.obj_decoder,
    "Locations":Locations_def._Type.obj_decoder
}

class Objects(object):
    """
    Wrapper that creates all the objects defined in Types folder using 
    TDM-Objects.init file to decide what objects are available.
    """
    def __init__(self):
        """
        Start an object and automatically load the input values
        """
        # Define a logger
        self.logger = logging.getLogger("Objects")
        self.logger.info("Creating Objects")

        # Get path variables, using absolute extension
        self.curr = os.path.abspath(__file__)
        # Find all instances of slanted values, # Note this means that the 
        # system only works on unix
        loc = [pos for pos, char in enumerate(self.curr) if char=='/']
        self.curr = self.curr[:loc[-1]+1]
        def_file = self.curr + "Objects.init"

        # Create an empty dictionary for all objects
        self.objects = {}
        # Load action types to be created as defined in Objects.init
        self.logger.debug("def file: {}".format(def_file))
        with open(def_file, 'rb') as fid:
            for line in fid:
                self.objects[line.strip('\n')] = {}

        for _type in self.objects.keys():
            self.build_objects(_type)

        self.logger.info("Objects have been built")

    def build_objects(self, _type):
        """
        Build specific type of object. Based on types inserted into 
        class using information from Objects.init
        """
        
        self.logger.debug("Loading type : {}".format(_type))
        obj_dec = decoder[_type]

        for file in os.listdir(self.curr+'/'+_type+"/"):
            if os.path.splitext(file)[1] == ".json":
                self.logger.debug("\tFile: {}".format(file))
                with open(self.curr+"/"+_type+"/"+file) as fid:
                    tmp_obj = json.loads(fid.read(),
                                         object_hook = obj_dec)
                    self.objects[_type][tmp_obj.name]=tmp_obj

    def new_object(self, _dict):
        """
        Create an template object for the TDM to work on
        """
        _type = _dict["Type"]
        _name = _dict["Name"]
        new_obj = copy.deepcopy(self.objects[_type][_name])
        return new_obj

class ActionStack(object):
    """
    A task dialog manager for the action stack storing the list of actions
    the current task requires the TDM to perform.
    """
    def __init__(self, MEx):
        """
        Initialize the action stack. Input also the dictionary MEx to search
        the word stack.
        """
        self.stack = []
        self.stack_size = 0

        self.logger = logging.getLogger("ActionStack")
        self.logger.info("Creating action stack")
        self.ErrorCount = 0

        self.MEx = MEx

    def add(self, action):
        """
        Add an object of tye Type : action to the stack. Add meta data to
        stack. 
        """
        self.stack.append(action)
        self.logger.info("Added to action stack : {}".format(action.name))
        self.stack_size += 1


    def pop(self):
        """
        Remove the top of the stack. Assuming the action has been performed
        """
        if self.stack_size > 0:
            temp = self.stack.pop(0)
            self.logger.info("Removed from action stack:{}".format(temp.name))
            self.stack_size -= 1

    def clean(self):
        """
        Remove all values from action stack
        """
        while not self.isEmpty():
            self.pop()
 
    def isEmpty(self):
        """
        Return true if stack is empty, false othervise
        """
        if self.stack_size == 0:
            return True
        return False
    
    def info_check(self, word_bag):
        # check if top of action stack has the information required
        self.logger.debug("Checking for information, stack size: {}".format(self.stack_size))
        if not self.isEmpty():
            action = self.stack[0]
            self.logger.debug("Running datasearch on {}, is question {}, task name {}".format(
                action.name, action.question, action.name))
            if action.question:
                # If the action has question i.e. requires information 
                # check if possible answer is in word bag, otherwise 
                # give the system a question to ask the user
                print "Current action : {}".format(action.name)
                print "Current action keywords {}".format(action.keywords)
                p = self.MEx.dict_search(action.keywords, word_bag)
                if p.sum() > 0:
                    return True, p
                elif p.sum() == 0:
                    self.ErrorCount += 1
                    return False, 0
                None
            else:
                # If there are no questions then this action ca
                return True, -1
                
        else :
            self.ErrorCount += 1
            return False 

    def run_action(self, task, p):
        """
        Run an action from the stack. Input the probability computation
        from info_check so that the information isn't computed twice
        """
        if not self.isEmpty():
            action = self.stack[0]
            
            # - - - - - - MAIN INPUT - - - - - - - - - #
            _dict = {}
            _dict["action"] = action
            _dict["p"]      = p
            if action.name == "talk":
                _dict["out_msg"] = task.out_strings[
                    np.random.randint(0, len(task.out_strings))
                ]


            return action.run(_dict)
        else : 
            self.ErrorCount += 1
            return {"Fail":True, "Reason":"RunActionNotAvailable:StackEmpty"}
    
    def get_info(self, task):
        """
        Create a question based on the top level task and the current action
        to ask the user so that information relevant to the action can be found
        """
        # TODO, encode this into both Tasks, additional questioning and
        # the actions. Additional words to explain
        self.logger.debug("Running get info for task: {}".format(task.name))
        if not self.isEmpty():
            action = self.stack[0]
            rand_q = task.out_strings[
                np.random.randint(0, len(task.out_strings))
            ]
            out_str = "Trying to solve object: {}".format(rand_q)
            return {"Result":"Talk", "Text":out_str}

    def getErrorCount(self):
        return self.ErrorCount
    def resetErrorCount(self):
        self.ErrorCount = 0
    

class Word_Bag(object):
    """
    A class storing the input words. Taking care of new input values. Cleaning
    the sentences and returning relevant values.
    """

    def __init__(self):
        self.logger = logging.getLogger("Word_Bag")
        self.logger.info("Creating Word Bag")

        self.access_time = None
        self.new_words = False
        self.len = 0

        self.buffer = []
        

    def add(self, sentence):
        """
        Scrub and add a sentence
        """
        if sentence != None and sentence != "":
            sentence = sentence.lower().split(" ")
            self.buffer.insert(0, sentence)
            self.logger.info("Adding sentence: {}".format(sentence))
            self.len += 1
            self.new_words = True
            self.access_time = timer()


    def get(self, no=0):
        if no <= self.len:
            self.new_words = False
            return self.buffer[no]
        return {"Fail":True, "Reson":"ValueError:OutOfRange"}

    def clean(self):
        self.logger.info("Cleaning Word_Bag")
        self.new_words = False
        self.buffer = []
        self.len = 0

    def elapsed(self):
        if self.access_time != None:
            return timer()-self.access_time
        else :
            return 0 

