# checkPrerequisites.py
# A function for checking prerequisites of a given data structure
# the input is a string name and module, the local function compares the 
# string to a database, sees where the data can be found and returns 
# True if data is availible, False if data is not found

import json

def checkPrerequisites(*args):
    # Given a string in, compare the string to known database
    # see where to look for the data. Return True if data is 
    # availible False if not found
    strIn = args[0]
    debug = args[1] # Turn debug mode on/off 1/0
    book = {}
    with open('dataLocation', 'r') as fobj:
        book = json.load(fobj)
        # Initially I was going to use try except, but decided it's better
        # when debugging to have the system crash here. If there is any errors
        # Question : as 
        if debug == 1:
            print("DEBUG: checkPrerequisites:checkPrerequisites =" + strIn)
    return functionMapper(book[strIn], debug)
        

def functionMapper(*args):
    # Given a specific name run the function
    funName = args[0]
    # Check to see if we are in debug mode
    debug   = args[1]

    if funName == "YTTM.myTurn":
        # TODO impliment by checking the YTTM through psyclone
        # and returning true if the YTTM decides that it is my turn
        return True, "" # Set to true for debugging purposes
    elif funName == "VISION.person":
        return True, "" # Set to true for debugging purposes
    elif funName == "GLOBAL.OK":
        return True, "" # Set to true for debuggin reasons.
    elif funName == "YTTM.OtherHasTurn":
        return True, ""


# Debug, if the function is run as a standalone, then print out the current
# dictionary, or chose the specific test cases
if __name__ == "__main__":
    
    debug = True
    testCases = ["myTurn", "isPerson"]
    for strIn in testCases:
        print(checkPrerequisites(strIn, debug))
