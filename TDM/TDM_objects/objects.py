#!/usr/bin/env python
#################################################################################
#     File Name           :     ../TDM_objects.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-06 17:14]
#     Last Modified       :     [2018-03-12 11:08]
#     Description         :     Objects specifically used by the TDM method 
#     Version             :     0.1
#################################################################################

from timeit import default_timer as timer
import logging
import os, sys
import copy
import json
import random
import numpy as np

class Dialog(object):
    """
    Stores information about when dialog was started, and if
    dialog is active
    """

    def __init__(self):
        self.logger = logging.getLogger("Dialog")
        self.logger.debug("Creating dialog object")
        self.start_time = None
        self.in_dialog = False
        self.active = False

    def on(self):
        self.logger.debug("Setting dialog object on")
        self.in_dialog = True

    def off(self):
        self.logger.debug("Setting dialog object off")
        self.in_dialog = False

    def status(self):
        return self.in_dialog

    def elapsed(self):
        if self.start_time is None:
            return 0
        else :
            return self.start_time - self.start_time
# # # # # # # # # # # # # # # # # # # # # # # # # # #   
# # # # # # # ACTION OBJECTS  # # # # # # # # # # # #   
# # # # # # # # # # # # # # # # # # # # # # # # # # #   

class Action_Parent(object):
    """
    Parent class for the action objects
    """
    def __init__(self):
        self.active = False
        self.msg = ""
        self.start_time = None
        self.action_id = -1
        self.timeout = False
        self.type = None

        self.hold_the_line = False
        self.finished = False
        

        # Set max time, overwrite in other functions
        self.max_time = 10

    def set_type(self, _type):
        self.type = _type 

    def set_id(self, id):
        self.action_id = id

    def id(self):
        return self.action_id

    def set_max_time(self, max_time):
        self.max_time = max_time

    def start_timer(self):
        self.start_time = timer()

    def set_msg(self, msg):
        self.msg = msg

    def remaining(self):
        if self.start_time is None:
            return 0
        else :
            return self.max_time - (timer()-self.start_time)

    def timeout_check(self):
        return self.timeout
    
    def timer(self):
        if self.start_time == None:
            return 0
        return timer() - self.start_time

    def elapsed(self):
        if self.start_time is None:
            return False
        if timer() - self.start_time > self.max_time:
            self.timeout = True
            return True
        return False
    
    def set_hold(self, tf):
        # tf = True/False
        self.hold_the_line = tf

    def get_holds(self):
        return self.hold_the_line

    def finish(self):
        self.finished = True


class Move_object(Action_Parent):
    """
    An object that encodes all possible points and returns the values
    depending on input control function
    """

    def __init__(self):
        Action_Parent.__init__(self)
        self.logger = logging.getLogger("Move_object")

        self.logger.debug("Created move object")
        self.set_hold("True")
        self.set_type("move")
        self.point = None
        self.set_max_time(3)

        """
        msg value should be definied by the location point that is selected

        possible point names(06.03.18)
            ControlPanel1
            ControlPanel2
        """

    def set_by_keyword(self, keyword, task_id):
        """
        Set the values by a keyword definition
        """
        self.logger.debug("Input to Move_Object: {}".format(keyword))
        self.set_id(task_id)

        if keyword== "Point1":
            self.msg = self.point1_set_location()
            self.point = "ControlPanel1"

        elif keyword == "Point2":
            self.msg = self.point2_set_location()
            self.point = "ControlPanel2"

    def point1_set_location(self):
        """
        Return a random sentance describing the action at hand
        """
        sentences = [
            "Will try to send controller to that location",
            "Will move controller to point 1",
            "Will move controller to there"
        ]
        return sentences[ np.random.randint(0,len(sentences)) ]

    def point2_set_location(self):
        """
        Return a random sentance describing the action at hand

        """
        sentences = [
            "Will try to send controller there ",
            "Will move controller to the second location",
            "The other robot, I will send it to that location"
        ]
        return sentences[ np.random.randint(0 ,len(sentences)) ]
    

class Talk_object(Action_Parent):

    def __init__(self):
        Action_Parent.__init__(self)
        self.logger = logging.getLogger("Talk_object")
        self.logger.debug("Created talk object")
        self.set_type("talk")
        self.set_max_time(15)
        self.set_hold(False)



    def set_string(self, sentence, task_id):
        # TODO : Connect to the TDM output.
        self.logger.debug("Adding output to talk object: {}".format(sentence))
        self.set_msg(sentence)
    
        # Dynamically allocate maximum time of sentence, based on 
        beta = .05
        self.set_max_time(len(sentence)*beta+1)


class Screen_navigation_object(Action_Parent):

    """
    Object that is used for screen navigation. 
    This object differs from move and talk in that 
        1) It doesn't finish automatically, it's stuck as Task PanelA until
            exited (either by timeout or manual)
        2) The main object (Screen_navigation_object) isn't actually put on
            action stack. Instead the object stores the output object, 
            specifically Panel_query object, in memory and sends that out.
    """
    class Panel_active(object):
        def __init__(self):
            self.stack = []

        def add(self, id):
            self.stack.append(id)

        def pop(self, id):
            if self.stack != []:
                if id == self.stack[0]:
                    self.stack.pop(0)

    class Window_Values(object):
        """
        Stores the values returned buy the panel query
        """
        def __init__(self):
            self.got = False
            self.time_added = -1
            self.data = []

        def add(self, msg):
            """
            input the keywords of the input message type into the 
            system
            """
            self.got = True
            self.time_added = timer()


        def get(self):
            self.got = False

            
    class Panel_query(Action_Parent):
        def __init__(self, active_panel):
            # Pointer to active panel values so that the object can
            # remove itself from the system once it is finished
            self.active_panels = active_panel

            # Init varaiblese
            Action_Parent.__init__(self)
            self.set_hold("False")
            self.type = "screen_msg"

        def set_msg(self, msg, id):
            self.msg = msg
            self.action_id = id
            self.active_panels.add(id)

        def finish(self):
            self.active_panels.pop(0)


    def __init__(self):
        Action_Parent.__init__(self)

        self.logger = logging.getLogger("Screen_navigator")
        self.logger.debug("Created a screen navigation object")

        self.set_type("Panel")
        self.set_max_time(0)
        self.set_hold(False)
        self.active_tasks = Screen_navigation_object.Panel_active()
        obj.current_panel_screen = Screen_navigation_object.Window_Values()


    def reset_screen(self, obj):
        action_id = obj.id()
        out_obj = Screen_navigation_object.Panel_query(self.active_tasks)
        obj.action_stack.add(out_obj)

    def set_by_keyword(self, keyword):
        """
        Define output of function by search keyword
        """
        self.logger.debug("Selecting output by keyword : {}".format(keyword))


    def query_screen(self, obj):
        """
        Get the current screen information
        """
        self.logger.debug("Querying the screen object")
        out_obj = Screen_navigation_object.Panel_query(self.active_tasks)
        task_id = obj.id()
        out_obj.set_msg("Query", task_id)
        out_obj.set_hold("True")
        out_obj.max_time(3)
        obj.action_stack.add(out_obj)





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # OTHER OBJECTS # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Word_Bag(object):
    """
    A class storing the input words. Taking care of new input values. Cleaning
    the sentences and returning relevant values.
    """
    class Input_Sentence(object):
        def __init__(self, sentence):
            self.sentence = sentence
            self.added = timer()

        def elapsed(self):
            # NOTE : Here we set the lifetime of a sentence in
            # the system
            if timer() - self.added > 15:
                return True
            return False
        
        def get(self):
            return self.sentence

    def __init__(self):
        self.logger = logging.getLogger("Word_Bag")
        self.logger.info("Creating Word Bag")

        self.new_words = False
        self.len = 0
        self.buffer = []
        
    def add(self, sentence):

        """
        Scrub and add a sentence
        """
        if sentence != None and sentence != "":
            sentence_object = Word_Bag.Input_Sentence(sentence.lower().split(" "))
            self.buffer.insert(0, sentence_object)
            self.logger.debug("Adding sentence: {}".format(sentence_object.get()))
            self.len += 1
            self.new_words = True
            self.clean()

    def get(self, no=0):
        self.clean()
        if self.buffer != [] and no <= len(self.buffer):
            self.new_words = False
            return self.buffer[no].get()
        return "" 
    
    def clean(self):
        for idx, obj in enumerate(self.buffer):
            if obj.elapsed():
                self.buffer = self.buffer[:idx]
                self.len = idx
                if idx == 0:
                    self.empty_bag()
                break

    def printall(self):
        if self.buffer != []:
            for sent in self.buffer:
                print "{} - {}".format(sent.get(), sent.elapsed())
        else:
            print "Word bag is empty"


    def empty_bag(self):
        self.logger.info("Cleaning Word_Bag")
        self.new_words = False
        self.buffer = []
        self.len = 0


if __name__ == "__main__":
    from Tasks import Task_object
    obj = Task_object()

    task = obj.get("GetObjective")
    print task.name
    print 20*"-"
    for k in range(10):
        print task.primary_question()
    print 20*"-"

    for k in range(10):
        print task.secondary_question()
    print 20*"-"

    for k in range(10):
        print task.timeout_question()
