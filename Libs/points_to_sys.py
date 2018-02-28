#! /usr/bin/env python
#################################################################################
#     File Name           :     points_to_sys.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-23 14:49]
#     Last Modified       :     [2018-02-26 11:16]
#     Description         :     Read the DEMO_points file and print 
#                               in the right output format so that
#                               they can be inserted into system.inc file
#     Version             :     0.1
#################################################################################

import os
import re
import numpy as np


class XMLName(object):
    def __init__(self, name):
        self.name = name
        self.attribs = 4*[None]
        self.count = 0
        self.overlap = []

    def add(self, value):
        self.attribs[self.count] = value.rstrip()
        self.count += 1

    def set_overlap(self, val):
        val=val.strip("[]")
        self.overlap.append(val)


    def _write(self, no):
        str1 = '<variable name="VantagePoint{}Name" value="{}" />'.format(
            no, self.name
        )
        attr_str = ""
        for idx,val in enumerate(self.attribs):
            if idx == 3:
                attr_str += val
            else:
                attr_str += val+", "

        str2 = '<variable name="VantagePoint{}Data" value="{}" />'.format(
            no, attr_str 
        )

        str3 = '<variable name="VantagePoint{}Overlap" value="{}" />'.format(
            no, self.overlap[0]
        )
        print str1
        print str2
        print str3


n = 7
counter = 0
lines = None
with open("DEMO_points", 'rb') as fid:
    lines = fid.readlines()

liter = iter(lines)
rm_mat = np.roll(np.eye(7),1, axis=1)
overlap = np.ones(7) -rm_mat
ovl_str = []

for line in overlap:
    tmp = ""
    for idx,val in enumerate(line):
        if val == 0:
            out = "0.0"
        elif val == 1:
            out = "1.0"

        if idx == len(line) -1:

            tmp += out
        else:
            tmp += out + ', '
    ovl_str.append(tmp)


for line in liter: 
    if line[0].isupper():
        name = line[:-2]
        new_item = XMLName(name)
        for i in range(4):
            tmp = next(liter).split("\t")
            new_item.add(tmp[1])

        if counter <= n:
            new_item.set_overlap(ovl_str[counter])
        else:
            new_item.set_overlap("0")

        new_item._write(counter+1)
        counter += 1



