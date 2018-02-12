#! /usr/bin/env python
#################################################################################
#     File Name           :     cleanup.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-09 11:31]
#     Last Modified       :     [2018-02-09 11:33]
#     Description         :     Clean up log files in the directory that
#                                   have become absolete
#     Version             :     0.1
#################################################################################

import os

os.system('find . -name "*.log" -exec rm {} \;')
