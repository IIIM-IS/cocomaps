#!/usr/bin/python2.7
"""
01.02.18
Author
    David Orn : david@iiim.is
    
Objective
    Special objects, points, pointing to information on the map. Define 
    keywords regarding each point. Output sentances that can steer the 
    user into giving relevant information
"""






class _Type(object):
    """
    Store each point in an object
    """
    def __init__(self, _type, name, description, 
                 dictionary, x, y, ow, oz):
        self._type = _type
        self.name = name
        self.description = description
        self.dictionary = dictionary
        self.x = x
        self.y = y
        self.ow = ow
        self.oz = oz

    
    @staticmethod
    def obj_decoder(obj):
        """
        Decoding function for the action _type 
        """
        if "_type" in obj and obj["_type"]=="Location":
            return _Type(obj["_type"], obj["name"], obj["description"],
                         obj["dictionary"], obj["x"], obj["y"], 
                         obj["ow"],obj["oz"])
        return obj
        
