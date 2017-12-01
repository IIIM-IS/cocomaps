#!/usr/bin/env python
#customXMLparser.py
"""
This is a custom xml parser, reader and writer(to be implimented) for the cocomaps project.
The current setup is rather confusing and hard to access the variables, all variables
are in the string form but can represent other values, ints, floats etc. 

Author
        David Orn
        david@iiim.is
(c)
        IIIM
Date created
        29.11.17     
"""

import os, sys
import xml.etree.ElementTree as ET
import pickle


class CoCoMapsXMLParser(object):
    def __init__(self, file_name):
        """
        Parse data based ont the CMLabs parsing rules
        """
        tree = ET.parse(file_name)
        self.root = tree.getroot()

    def keyword_print(self, keyword): 
        """
        Search the parser for a specific type
        print values
        """
        if keyword == "point":
            self.point()
        else :
            for value in self.root.iter(keyword):
                print value.tag, value.attrib

    def point(self):
        """
        This script was originally run for this special process, it parses the location of the points to 
        a simpler form and save the file as txt. The reason is to work further with specific
        values
        """
        output = {}
        for point in self.root.iter("point"):
            output[point.attrib['id']] = [point.attrib['data'], point.attrib['overlap']]

        with open("points.pkl", 'wb') as fout:
            pickle.dump(output, fout, pickle.HIGHEST_PROTOCOL)




if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        key_to_parse = sys.argv[2]
        Parser = CoCoMapsXMLParser(file_name)
        Parser.keyword_print(key_to_parse)
    else :
        print "Found no file name"

