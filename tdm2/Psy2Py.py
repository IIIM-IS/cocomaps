# Python module for reading Psyclone whiteboards. Sending and
# retrieving relivant information

# Author : David Orn = david@iiim.is

from threading import Thread
import time

def getMillis():
    return int(round(time.time()*1000))

class PsycloneList(Thread):
    # Create a special thread that monitors psyclone and
    # input/output messages

    # HOWTO use
    # Create an instance of class PsycloneList, (do I need to 
    # start it from main loop?) call item (of class PsycloneList)
    # using item.readList.

    def __init__(self):
        Thread.__init__(self)
        self.List = None
        self.LastCheck = getMillis()
        self.debugCounter = 1
        self.bit = 1
        self.daemon = True
        self.sleepTime = .1


    def setList(self):
        self.List = self.readPsyclone()

    def readList(self):
        return self.List

    def run(self):
        while True:
            self.setList()
            time.sleep(self.sleepTime)

    def readPsyclone(self):
        # Todo impliment with connectecion to psycline
        debug = 1 # Set to 1 while debugging and 0 
                  # if psyclone is up and running
        if debug == 1:
            out = []
            # Flip between different output messages
            if self.debugCounter % 1000 == 0:
                self.debugCounter = 1
                # Flip bit every 500 ~= 50 sek
                self.bit = -self.bit

            if self.bit > 0:
                out = ["[head-motor-on]", "[audio-input]"]
            elif self.bit < 0:
                out = ["[audio-input]","[Listen-To]", "[head-motor-on]"]
            self.debugCounter += 1
            return out
        # TODO need to add the connector with psyclone
        elif debug == 0:
            return None


