# Checking if prerequisites are met, 
# Author = David Orn : david@iiim.is

import InfoBag
import logging 
logger = logging.getLogger(__name__)


def personFound(*args):
    # If argument is empty, check to see if person has 
    # been found, argument is given, set the current
    # result to the bag item, personFound
    if args:
        print("RUNS if args")
        InfoBag.Bag["personFound"] = args[0]
    return InfoBag.Bag["personFound"]

def personNotFound(*args):
    return not InfoBag.Bag["personFound"]

def haveGreeted(*args):
    if args:
            InfoBag.Bag["haveGreeted"] = args[0]
    return InfoBag.Bag["haveGreeted"]

def haveNotGreeted(*args):
    logger.debug("InfoBag: " + str(InfoBag.Bag["haveGreeted"]))
    return not InfoBag.Bag["haveGreeted"]


def askingToMakeACall(*args):
    if args:
        InfoBag.Bag["askingToMakeACall"] = args[0]
    return InfoBag.Bag["askingToMakeACall"]


def askingToScheduleMeeting(*args):
    if args:
        InfoBag.askingToScheduleMeeting = args[0]
    return InfoBag.Bag["askingToScheduleMeeting"]


def talkingToPerson(*args):
    if args:
        InfoBag.talkingToPerson = args[0]
    return InfoBag.Bag["talkingToPerson"]


prerequisites = {
    "personFound" : personFound,
    "personNotFound" : personNotFound,
    "haveGreeted" : haveGreeted,
    "haveNotGreeted" : haveNotGreeted, 
    "askingToMakeACall": askingToMakeACall,
    "askingToScheduleMeeting" : askingToScheduleMeeting,
    "talkingToPerson" : talkingToPerson,
}

if __name__ == "__main__":
    fileLoc = "/home/david/IIIM/Reports/TDM_functions/"
    fName   = 'prerequisites.txt'
    with open(fileLoc+fName, 'w') as fid:
        for key in prerequisites.keys():
            outStr = " & " + str(key) +  " \\\\\n"
            fid.write(outStr)
            
