#! /usr/bin/env python
#################################################################################
#     File Name           :     temp.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-08 09:48]
#     Last Modified       :     [2018-03-09 15:30]
#     Description         :      
#     Version             :     0.1
#################################################################################


class temp(object):
    def __init__(self):
        self.val = True

    def setval(self, val):
        self.val = val



obj = temp()

print obj.val

obj.setval(False)

print obj.val
