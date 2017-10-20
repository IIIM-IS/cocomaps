# Checking if prerequisites are met, 
# Author = David Orn : david@iiim.is

import InfoBag


def personFound(*args):
    # If argument is empty, check to see if person has 
    # been found, argument is given, set the current
    # result to the bag item, personFound
    if len(*args) ==  1:
        InfoBag.Bag["personFound"] = args[0]
    return InfoBag.Bag["personFound"]


def haveGreeted(*args):
    if len(args) == 1:
        InfoBag.Bag["haveGreeted"] = args[0]
    return InfoBag.Bag["haveGreeted"]


def askingToMakeACall(*args):
    if len(args) == 1:
        InfoBag.Bag["askingToMakeACall"] = args[0]
    return InfoBag.Bag["askingToMakeACall"]


def askingToScheduleMeeting(*args):
    if len(args) == 1:
        InfoBag.askingToScheduleMeeting = args[0]
    return InfoBag.askingToScheduleMeeting


def talkingToPerson(*args):
    if len(args) == 1:
        InfoBag.talkingToPerson = args[0]
    return InfoBag.talkingToPerson


prerequisites = {
    "personFound" : personFound,
    "personNotFound" : personFound,
    "haveGreeted" : haveGreeted,
    "haveNotGreeted" : haveGreeted, 
    "askingToMakeACall": askingToMakeACall,
    "askingToScheduleMeeting" : askingToScheduleMeeting,
    "talkingToPerson" : talkingToPerson,
}
