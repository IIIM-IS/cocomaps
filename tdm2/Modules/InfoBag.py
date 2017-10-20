# InfoBag.py

# A bag container for much of required data

import time

def currentTime():
    return int(round(time.time()*1000))

# The InfoBag is a global, dynamic, bag that compiles information during runtime.
# Here we place any possible dynamical values and item specific functions.
global Bag

Bag={
        "lastAccess": [], # Store time when last accessed, some 
                          # items are time sensitive.
        "personName": [], 
        "haveGreeted": False,
        "personName" : [],
        "personFound" : False,
        "askingToMakeACall": False,
        "TalkingToPerson" : False

     }
