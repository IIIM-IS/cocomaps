#!/usr/bin/env python
#################################################################################
#     File Name           :     ../TDM_objects.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-06 17:14]
#     Last Modified       :     [2018-03-28 11:59]
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
        self.logger.debug("#TDM: Creating dialog object")
        self.start_time = None
        self.in_dialog = False
        self.active = False

    def on(self):
        self.logger.debug("#TDM: Setting dialog object on")
        self.in_dialog = True

    def off(self):
        self.logger.debug("#TDM: Setting dialog object off")
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
        self.logger.debug("#TDM: Created move object")
        self.set_hold("True")
        self.set_type("move")
        self.point = None
        self.set_max_time(35)

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
        self.logger.debug("#TDM: Input to Move_Object: {}".format(keyword))
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
        self.logger.debug("#TDM: Created talk object")
        self.set_type("talk")
        self.set_max_time(15)
        self.set_hold(False)
        self.level = 0

    def set_string(self, sentence, speach_id, level):
        # TODO : Connect to the TDM output.
        self.logger.debug("#TDM: Adding output to talk object: {}".format(sentence))
        self.set_msg(sentence)
        self.set_id(speach_id)
        self.level = level
        # Dynamically allocate maximum time of sentence, based on
        beta = 0
        # Depricated, moved into TDM_psyclone.TDM_speak()
        self.set_max_time(0)


class Panel_query(Action_Parent):
    def __init__(self) :
        # Pointer to active panel values so that the object can
        # remove itself from the system once it is finished
        Action_Parent.__init__(self)
        self.set_hold("False")
        self.type = "screen_msg"
        self.push_button = None

    def set_button_to_push(self, name):
        self.push_button = name


    def get_button_to_push(self):
        return self.push_button


    def set_msg(self, msg, id):
        self.msg = msg
        self.set_id(id)

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
    class Panel_active(Action_Parent):
        def __init__(self):
            Action_Parent.__init__(self)
            self.stack = []
            self.type = "Panel_active"

        def add(self, id):
            self.stack.append(id)
            self.set_id(id)

        def pop(self, id):
            if self.stack != []:
                if id == self.stack[0]:
                    self.stack.pop(0)


    def __init__(self):
        Action_Parent.__init__(self)

        self.logger = logging.getLogger("Screen_navigator")
        self.logger.debug("#TDM: Created a screen navigation object")

        self.set_type("Panel")
        self.set_max_time(5)

        self.set_hold(False)
        self.screen_name = None
        self.last_query_time = 0

    def get_last_query(self):
        return self.last_query_time

    def set_last_query(self, time):
        self.last_query_time = time

    def push_button(self, name, obj):
        self.logger.debug("#TDM: ScreenNav obj = Pushing button: {}".format(name))
        action_id = obj.id()
        panel_query = Panel_query()
        panel_query.set_max_time(5)
        panel_query.set_msg("PushButton", action_id)
        panel_query.set_button_to_push(name)
        obj.action_stack.add(panel_query)


    def reset_screen(self, obj):
        self.logger.debug("#TDM: ScreenNav obj = Resetting screen")
        action_id = obj.id()
        panel_query = Panel_query()
        panel_query.set_msg("Reset", action_id)
        panel_query.set_max_time(5)
        obj.action_stack.add(panel_query)


    def query_screen(self, obj):
        """
        Get the current screen informato
        """
        if timer() - self.get_last_query() > 1.5:
            self.set_last_query(timer())
            self.logger.debug("#TDM: ScreenNav obj = Querying screen")
            panel_query= Panel_query()
            action_id = obj.id()
            panel_query.set_msg("Query", action_id)
            panel_query.set_hold("True")
            panel_query.set_max_time(5)
            obj.action_stack.add(panel_query)

    def back_button(self, obj):
        action_id = obj.id()
        panel_query = Panel_query()
        panel_query.set_msg("BackButton", action_id)
        obj.action_stack.add(panel_query)


    def update(self, screen_name):
        """
        Define the current screen information based on the screen name
        keyword
        """
        self.screen_name = screen_name

class Pin_Query(Action_Parent):
    def __init__(self):
        Action_Parent.__init__(self)
        self.logger = logging.getLogger("PINLOG")
        self.set_type("PinQuery")
        self.in_queue = False
        self.set_hold("True")
        self.set_max_time(5)
        self.in_queue = False

    def add(self, value, obj):
        # send numeric value to panel, monitor if it returns passed
        # or failed
        panel_query = Panel_query()
        action_id = obj.id()
        panel_query.set_msg("Pin", action_id)
        panel_query.set_hold("True")
        panel_query.set_max_time(5)
        panel_query.set_button_to_push(value)
        obj.action_stack.add(panel_query)
        self.going_to_queue()

    def return_fail(self):
        self.passed = False

    def return_passed(self):
        self.logger.debug("#TDM Set passed on pin to true")
        self.passed = True

    def queueing(self):
        self.logger.debug("#TDM Set passed on pin to false")
        return self.in_queue

    def going_to_queue(self):
        self.in_queue = True

    def out_of_queue(self):
        self.in_queue = False


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
            self.logger.debug("#TDM: Adding sentence: {}".format(sentence_object.get()))
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
