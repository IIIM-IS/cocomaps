#!/usr/bin/python2.7
"""
01.02.18
Author
    David Orn : david@iiim.is

Objective
    Describe how to handle a task object, i.e. how to load and create a python
    struct from this specific _type.
"""

from Action_lib import action_dict
class _Type(object):
    """
    Type class, top level decision, selecting which tasks to get to
    and which actions to perform
    """
    def __init__(self, _type, name, description, out_strings, actions, pass_action):
        self._type = _type
        self.name = name
        self.description = description
        self.out_strings = out_strings
        self.actions     = actions
        self.pass_action = action_dict[pass_action]

        self.action_stack = None
        self.parent = None


    @staticmethod
    def obj_decoder(obj):
        """
        Decoder function for the json structure
        """
        if "_type" in obj and obj["_type"]=="Task":
            return _Type(obj["_type"], obj["name"], obj["description"], 
                        obj["out_strings"],  obj["actions"], obj["pass_action"])
            return obj
