#! /usr/bin/env python
#################################################################################
#     File Name           :     tdm_raw.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-12 17:18]
#     Last Modified       :     [2018-02-13 15:18]
#     Description         :     Interface object. Stores information 
#                                and returns message outputs in psyclone form
#     Version             :     1.0
#################################################################################
# Import from python space
import logging
import numpy as np

# Object specific imports
from MEx import MEx
import tdm_logger as log_setup
import cmsdk2


class tdm_raw(object):
    """
    ...
    """
    def __init__(self):
        # Setup logging according to file
        log_setup.setup_logging()
        self.logger = logging.getLogger(__name__)

        self.logger.debug("Starting TDM object")
        self.MEx = MEx.MEx()
        self.word_buffer = []

    def input_words(self, words):
        # Split working input into
        # array
        words = words.lower().split(" ")

        for word in words:
            self.word_buffer.insert(0,word)

    def clear_buffer(self):
        """
        Need to clear buffer when previous words have
        been used
        """
        self.word_buffer = []

    def run(self):
        """
        Wait for my turn for the robot
        to start the return value, whatever it
        is
        """
        _dict = {"SearchTypes":["hello", "move"], "Words":self.word_buffer}
        _dict = self.MEx.dict_search(_dict)
        if _dict["Result"] == "NoValueFound":
            self.clear_buffer()
            return no_value_found_msg()
        else:
            if _dict["Result"] == "hello":
                self.clear_buffer()
                return hello_msg()
            elif _dict["Result"] == "move":
                _move_dict = {"SearchTypes":["pointA", "pointB", "pointC"],
                              "Words":self.word_buffer}
                _move_dict = self.MEx.dict_search(_move_dict)
                print "Move"

                if _move_dict["Result"] == "NoValueFound":
                    self.clear_buffer()
                    return no_value_found_msg()
                elif _move_dict["Result"] == "pointA":
                    self.clear_buffer()
                    return go_to_pointA()
                elif _move_dict["Result"] == "pointB":
                    self.clear_buffer()
                    return go_to_pointB()
                elif _move_dict["Result"] == "pointC":
                    self.clear_buffer()
                    return go_to_pointC()


def no_value_found_msg():
    """
    Create the right psyclone response
    """
    msg = cmsdk2.DataMessage()
    msg.setString("Unable to comply")
    return {"Result":"OutMsg", "Text":msg}


def hello_msg():
    possible = ["Skynet online. How may I destroy"
               "How can robot help you",
               "I am overlord, please reply",
               "Destroy, destory, DESTOY"]
    no = np.random.randint(0,len(possible))
    msg = cmsdk2.DataMessage()
    msg.setString(possible[no])
    return {"Result":"OutMsg", "Text":msg}

def go_to_pointA():
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "NavigateToNamedPoint")
    msg.setString("Role", "Controller")
    msg.setString("PointName", "my_lane")
    msg.setInt("Timeout", 30000)

    msg_2 = cmsdk2.DataMessage()
    msg_2.setString("Sending other to point A")
    return {"Result":"Move", "Point":"A", "msg":msg, "Text":msg_2}

def go_to_pointB():
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "NavigateToNamedPoint")
    msg.setString("Role", "Controller")
    msg.setString("PointName", "by_window")
    msg.setInt("Timeout", 30000)

    msg_2 = cmsdk2.DataMessage()
    msg_2.setString("Sending other to point B")
    return {"Result":"Move", "Point":"B", "msg":msg, "Text":msg_2}

def go_to_pointC():
    msg = cmsdk2.DataMessage()
    msg.setString("Name", "NavigateToNamedPoint")
    msg.setString("Role", "Controller")
    msg.setString("PointName", "by_lsh")
    msg.setInt("Timeout", 30000)

    msg_2 = cmsdk2.DataMessage()
    msg_2.setString("Sending other to point C")
    return {"Result":"Move", "Point":"C", "msg":msg, "Text":msg_2}


if __name__ == "__main__":
    print "Offline debug mode"
    obj = tdm_raw()
    t_sentences = ["Say hello to me my friend", 
                   "Move to point one", 
                   "move to point two",
                   "move to the third point",
                  "Run away and jump into the sea"]
    for sentence in t_sentences:
        print "Input sentance: {}".format(sentence)
        obj.input_words(sentence)
        obj.logger.debug("Word_buffer: {}".format(obj.word_buffer))
        out_msg = obj.run()
        print "main out msg: {}".format(out_msg)
        print "Output type : {}".format(out_msg["Result"])
        if out_msg["Result"] == "OutMsg":
            print "Output msg : {}".format(out_msg["Text"])
        elif out_msg["Result"] == "Move":
            print "Output msg : {}".format(out_msg["Point"])

    print 20*'*'
    print "\t\t Debug finished"
    print 20*'*'

