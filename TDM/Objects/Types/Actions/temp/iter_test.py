#! /usr/bin/env python
#################################################################################
#     File Name           :     iter_test.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-09 15:07]
#     Last Modified       :     [2018-02-09 15:28]
#     Description         :      Testing methods of inplementing iterator
#     Version             :     0.1
#################################################################################



class temp(object):
    def __init__(self):
        self.iter_value = 0
        self.values = range(10)

    def __iter__(self):
        return self

    def next(self):
        if self.iter_value >= len(self.values):
            self.iter_value = 0
            raise StopIteration
        ret_value = self.values[self.iter_value]
        self.iter_value += 1
        return ret_value






obj = temp()
for k in range(3):
    for val in obj:
        print val


