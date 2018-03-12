#!/usr/bin/env python
#################################################################################
#     File Name           :     SI_tasks.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-07 11:11]
#     Last Modified       :     [2018-03-10 09:21]
#     Description         :      
#     Version             :     0.1
#################################################################################

import logging, json, os, random, copy
from timeit import default_timer as timer
import numpy as np
import actionlib



# # # # # # # # # # # # # # # # # # # # # # # # # # #   
# # # # # # # TASK  OBJECTS  # # # # # # # # # # # #   
# # # # # # # # # # # # # # # # # # # # # # # # # # #   

class Questions(object):
    """
    A specific iterator for the questions 
    """
    def __init__(self, struct):
        self.primary_ = struct["primary"]
        self.secondary_ = struct["secondary"]
        self.timeout_ = struct["timeout"]
        self.n_primary = range(0, len(self.primary_))
        random.shuffle(self.n_primary)

        self.n_secondary = range(0,len(self.secondary_))
        random.shuffle(self.n_secondary)

        self.n_timeout   = range(0,len(self.timeout_))
        random.shuffle(self.n_timeout)

        self.prim_loc = 0
        self.sec_loc  = 0
        self.tim_loc  = 0

    def set_primary(self, sentence):
        print "Setting new primary question as {}".format(sentence)
        # Overwrite the json file with a new sentence
        self.primary_ = []
        self.primary_.append(sentence)
        self.n_primary = [0]
        self.prim_loc = 0

    def  set_secondary(self, sentence):
        self.secondary_ = []
        self.secondary_.append(sentence)
        self.n_secondary = [0]
        self.sec_loc = 0

    def primary(self):
        if self.n_primary == []:
            return ""
        if self.prim_loc > len(self.primary_)-1:
            self.prim_loc = 0
            random.shuffle(self.n_primary)
        out_string = self.primary_[self.n_primary[self.prim_loc]]
        self.prim_loc += 1
        return out_string 


    def secondary(self):
        if self.n_secondary == []:
            return ""
        if self.sec_loc > len(self.secondary_)-1:
            self.sec_loc = 0
            random.shuffle(self.n_secondary)
        out_string = self.secondary_[self.n_secondary[self.sec_loc]]
        self.sec_loc += 1
        return out_string

    def timeout(self):
        if self.n_timeout == []:
            return ""
        if self.tim_loc > len(self.timeout_)-1:
            self.tim_loc= 0
            random.shuffle(self.n_timeout)
        out_string = self.timeout_[self.n_timeout[self.tim_loc]]
        self.tim_loc += 1
        return out_string


class Task(object):
    def __init__(self, obj):
        self.logger = logging.getLogger("TaskCreator")
        self.name = obj["name"]
        self.logger.debug("Adding task {}".format(self.name))
        self.keywords = obj["keywords"]
        self.keylist = []
        if self.keywords != None:
            for key in self.keywords.keys():
                self.keylist.append(key)
        self.questions = Questions(obj["questions"])
        self.keyword = None 
        self.storage = None
        
        # Task specific information
        if self.name == "Greet":
            self.keyword = "Nothing"
            self.eval = actionlib.action_greet
        elif self.name == "GetObjective":
            self.eval = actionlib.action_get_objective
        elif self.name == "Move":
            self.eval = actionlib.action_movement
        elif self.name == "KnockKnock":
            self.eval = actionlib.action_knockknock
            joke = self.secondary_question()
            self.part1 = joke[0]
            self.part2 = joke[1]
            self.additional_question = joke[2]
        elif self.name == "StartGen":
            self.eval = actionlib.action_startgen

        elif self.name == "PanelA":
            self.eval = actionlib.action_PanelA

        self.accessed = 0
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def store(self, object):
        self.storage = object

    def get_stored(self):
        return self.storage

    def access(self):
        self.accessed += 1

    def clear_keyword(self):
        self.keyword = None

    def set_keyword(self, keyword):
        self.keyword  = keyword


    def primary_question(self):
        return self.questions.primary()

    def secondary_question(self):
        return self.questions.secondary()
        
    def timeout_question(self):
        return self.questions.timeout()



class Task_object(object):
    """
    Create a wrapper around the task objects
    """
    def __init__(self):

        self.logger = logging.getLogger("Task_object")
        self.logger.debug("Starting Task object. Creating objects")
        self.Tasks = {}

        curr = str(os.path.abspath(__file__))
        loc = [pos for pos, char in enumerate(curr) if char=='/']           
        curr = curr[:loc[-1]+1]   
        file_loc = curr + "tasks/"
        for file in os.listdir(file_loc):
            if os.path.splitext(file)[1] == ".json":
                file_path = file_loc + file
                self.logger.info("Parsing file: {}".format(file_path))
                data = json.load(open(file_path))
                obj = Task(data)
                self.Tasks[obj.name] = obj

    def get(self, name):
        """
        Get a clean copy of the Task in questions
        """
        obj = copy.copy(self.Tasks[name])
        return obj

if __name__ == "__main__":
    obj = Task_object()
