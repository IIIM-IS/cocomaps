#!/usr/bin/python2.7
"""
01.02.18
Author
    David Orn : david@iiim.is
    
Objective
    Map a json description to actionables. Try to act out these actions 
    and return True/False depending on how it worked
"""

class _Type(object):
    """
    Object type action. Defines the set of actions that the object is
    associated with
    """
    def __init__(self, _type, name, description, function_call):
        self._type = _type
        self.name = name
        self.description = description
        self.function_call = function_call

    
    @staticmethod
    def obj_decoder(obj):
        """
        Decoding function for the action type 
        """
        if "_type" in obj and obj["_type"]=="Action":
            return _Type(obj["_type"], obj["name"], obj["description"],
                        obj["function_call"])
        
