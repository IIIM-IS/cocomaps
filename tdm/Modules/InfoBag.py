# InfoBag.py

# A bag container for much of required data


# The InfoBag is a global, dynamic, bag that compiles information during runtime.
# Here we place any possible dynamical values and item specific functions.
global Bag

Bag={
        "lastAccess"        : [], # Store time when last accessed, some 
                          # items are time sensitive.
        "personName"        : "David Johannesson", 
        "haveGreeted"       : False,
        "personFound"       : False,
        "askingToMakeACall" : False,
        "talkingToPerson"   : False,
    "askingToScheduleMeeting": False,
        "lastUtterance"     : ""
     }
