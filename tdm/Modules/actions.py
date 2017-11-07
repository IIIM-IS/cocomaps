# actions.py
# A function dictionary, here new actions can be implimented
# added to the dictionary and called instantly

import logging, sys
import numpy as np
from TaskHandler import static as static
from Modules import InfoBag
import Modules as TaskHandler

# Get MEx form one level up
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
from MEx import MEx

logger = logging.getLogger(__name__)
def getObjective(*args):
    # A main objective task, get input objective
    '''
    Meta task
    This is the initial function called when instigating a 
    dialogue between robot and person
    '''
    inVal = raw_input(10*'*'+"What would you like me to do"+10*'*'+'\n')
    InfoBag.Bag["lastUtterance"]=inVal

    logger.debug("GetObjective running:")
    logger.debug(inVal)

    MExObject = MEx.MEx(str(inVal), ["task"])
    value = MExObject.value

    
    returnValue = False
    errMsg = ''

    newTask = static.tasks[value]
    newTask = TaskHandler.TaskHandler.TaskHandler(newTask)
    val, res = newTask.run()

    try : 
        logger.debug("Trying to run value: "+ str(value))
        newTask = static.tasks[value]
        newTask = TaskHandler.TaskHandler.TaskHandler(newTask)
        returnValue, errMsg = newTask.run()
        logger.debug("Finished correctly")

    except :
        logger.info("ERROR: actions.py unknown new taks")
        logger.info(value)
        logger.info(sys.exc_info()[0])

    return returnValue, errMsg


def greetPerson(*args):
    # An action where robot greets person
    '''
    This task is run when a person has been identified
    it greets person
    '''
    possible = ["Good day", "Hello", "Howdy", "Nice Weather ey"]
    if not InfoBag.Bag["haveGreeted"]:
        print(10*'*' + possible[np.random.randint(len(possible))] + 10*'*')
        InfoBag.Bag["haveGreeted"] = True
        return True, ""
    #iInfoBag.Bag["haveGreeted"] = True
    return False, "actions:greetPerson not implemented"


def answerQuestion(*args):
    '''
    NOT IMPLEMENTED
    This function starts a subprogram allowing for input of question
    through voice and output of answer through audio
    Author : david@iiim.is
    '''
    inVal = raw_input("What would you like to know")
    return True, "actions.askMeAnything not implemented"

def headTurn(direction):
    '''
    NOT IMPLEMENTED
    This function decides, based on the name of the task calling it,
    which direction to move (task TurnLeft turns left etc.) 
    Author : david@iiim.is
    '''
    # Make the robot turn in one direction, based on which
    # task calls, 
    if direction.name == "TurnLeft":
        # TODO turn left
        print("Turning left")
    elif direction.name == "TurnRight":
        # TODO turn right
        print("Turning right")
    elif direction.name == "FaceForwards":
        # TODO face robot forwards
        print("Facing forwards")

    return True, "actions:headTurn not implemented"


def scheduleMeeting(*args):
    # A meeting needs three things, 
    #   Participants
    #   Location
    #   Time
    
    print("Allright let's schedule a meeting " + InfoBag.Bag["personName"])
    # If we want to add memory then we can pull the last
    # utterance from InfoBag.
    
    ## WHO
    
    ## Where

    ## When 
    raw_input("Who would you like to meet? \n")
    
    return True, ""

def makeACall():
    pass

    
actions = {
    "scheduleMeeting"   : scheduleMeeting,
    "answerQuestion"    : answerQuestion,
    "makeACall"         : makeACall,
    "getObjective"      : getObjective,
    "headTurn"          : headTurn,
    "greetPerson"       : greetPerson
}



if __name__ == "__main__":
    keyList = []
    for key in actions:
        keyList.append(key)

    keyList.sort()
    with open("/home/david/IIIM/Reports/TDM_functions/actionsList.tex", 'w') as fid:
        for key in keyList:
            print(key)
#            fid.write("&"+ key+ " \\\\ \n")

#    task1= debugClass("TurnLeft")
#    task2= debugClass("TurnRight")
#    task3= debugClass("FaceForwards")
#    for key in actions.keys():
#        if key == "headTurn":
#            actions[key](task1)
#            actions[key](task2)
#            actions[key](task3)
#        else : 
#            actions[key]()

