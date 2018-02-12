#! /usr/bin/env python
#################################################################################
#     File Name           :     remove_list_test.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-09 11:54]
#     Last Modified       :     [2018-02-09 13:48]
#     Description         :      Testing to see how to use remove from list
#     Version             :     0.1
#################################################################################

import numpy as np

ll = []
for value in range(10):
    ll.append(value)


print ll

for rval in range(5):
    ll.pop(0)
    print ll

ll = []
for value in range(10):
    ll.insert(0,value)

print ll
