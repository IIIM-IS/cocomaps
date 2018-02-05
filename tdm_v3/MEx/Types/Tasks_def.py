#!/usr/bin/python2.7
"""
01.02.18
Author
    David Orn : david@iiim.is

Objective
    Describe how to handle a task object, i.e. how to load and create a python
    struct from this specific _type.
"""

class _Type(object):
    """
    Type class, top level decision, selecting which tasks to get to
    and which actions to perform
    """
    def __init__(self, _type, name, description, out_strings, fail_action,
                 pass_action, keywords, dictionary, max_time, max_tries,
                action):
        self._type = _type
        self.name = name
        self.description = description
        self.out_strings = out_strings
        self.fail_action = fail_action
        self.pass_action = pass_action
        self.keywords    = keywords
        self.dictionary  = dictionary
        self.max_time    = max_time
        self.max_tries   = max_tries
        self.action      = action

    @staticmethod
    def obj_decoder(obj):
        """
        Decoder function for the json structure
        """
        if "_type" in obj and obj["_type"]=="Task":
            return _Type(obj["_type"], obj["name"], obj["description"], 
                        obj["out_strings"], obj["fail_action"], 
                        obj["pass_action"], obj["keywords"], 
                        obj["dictionary"], obj["max_time"], 
                        obj["max_tries"], obj["action"])
            return obj
