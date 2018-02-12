#! /usr/bin/env python
#################################################################################
#     File Name           :     Objects.py
#     Created By          :     David Orn Johannesson
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-09 08:59]
#     Last Modified       :     [2018-02-12 11:45]
#     Description         :     An object holder for the different types
#                                   used inside TDM. Stores the values 
#                                   and defines type specific actions
#     Version             :     0.1
#################################################################################

import json
import os
import sys
import logging
import copy



# Import decoding methods
from Types import Actions_def
from Types import Tasks_def
from Types import Locations_def


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
        self.logger = logging.getLogger(__name__)
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

        for file in os.listdir(self.curr+"/Types/"+_type+"/"):
            if os.path.splitext(file)[1] == ".json":
                self.logger.debug("\tFile: {}".format(file))
                with open(self.curr+"/Types/"+_type+"/"+file) as fid:
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


if __name__=="__main__":
    sys.path.append("..")
    import tdm_logger
    tdm_logger.setup_logging()
    obj = Objects()




