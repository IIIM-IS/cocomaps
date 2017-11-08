#!/usr/bin/env python
# dualProcess.py
"""
A small definition of a function that takes in a fucntion handle
and input arguments and runs these in parallel and returns the one
that finishes first. 
The second one finishes in the queue but is lost forever. 
The objective is to be able to run two processes simultainously
where one process is time dependent.


Author :    David Orn 
            david@iiim.is
(c)IIIM : http://iiim.is

Created: 08.11.17
"""

import threading, time
import Queue


class ThreadItem(threading.Thread):
    def __init__(self, process, queue, *args):
        threading.Thread.__init__(self)
        # Not sure this works
        threading.Thread.daemon = True
        self.queue = queue
        self.process = process
        self.args = args

    def __getitem__(self):
        return self.process

    def run(self):
        result = self.process(self.args)
        self.queue.put(result)

def dualProcess(A, B, *args):
    Q = Queue.Queue()
    p1 = ThreadItem(A, Q, args[0])
    p2 = ThreadItem(B, Q, args[1])

    p1.start()
    p2.start()

    while Q.empty():
        None
    return Q.get()





# * * * DEBUGGING FUNCTIONS * * * * * *
def tA(*args):
    print("Starting A")
    time.sleep(5)
    return False, "Timer tA timout"

def tD(*args):
    print("Starting D")
    inp = raw_input("Give input")

    return True, inp
# * * * END OF DEBUGGING * * * * * *
if __name__ == "__main__":
    res = dualProcess(tA, tD, None, None)
    print(res)
