#!/usr/bin/env  python
# Multipass.py
"""
A threading module for the task dialogue manager (TDM). 

CLASS : 
    TimingProcess()
        Compares two functions, A & B, returns the results of the
        first function to finish. Used to create a timed effect, e.g.
        giving a question some maximum time limit that can be waited
        until stopped

Author
        David Orn Johannesson : david@iiim.is
(c)IIIM.is
"""
import time
from Queue import Queue
from threading import Thread


class RunObject(Thread):
    def __init__(self, process, queue):
        Thread.__init__(self)
        Thread.daemon = True
        self.process = process
        self.queue = queue

    def run():
        return self.process()

class TimingProcess():
    def __init__(self, A, B):
        self.queue = Queue()
        self.p1 = RunObject(A, self.queue)
        self.p2 = RunObject(B, self.queue)
        self.go()

    def go(self):
        self.p1.start()
        self.p2.start()

        print(self.queue.get())



def TestA():
    time.sleep(2)
    return "Finished A"

def TestB():
    time.sleep(3)
    return "Finished B"


if __name__ == "__main__":
   TimingProcess(TestA, TestB)

