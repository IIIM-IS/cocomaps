# actions.py
# A function dictionary, here new actions can be implimented
# added to the dictionary and called instantly
"""
Names of callable functions

actions[keyWord]
keyWord =
    "scheduleMeeting"  
    "answerQuestion"  
    "makeACall"      
    "getObjective"  
    "headTurn"     
    "greetPerson" 
"""
import logging, sys, os, time, select
import numpy as np
from timeit import default_timer as timer

from Modules import static as static, InfoBag, Timer
import Modules as TaskHandler
# Get MEx form one level up
parentdir = __file__[:-23]
os.sys.path.insert(0,parentdir)
import MEx.MEx as MEx


logger = logging.getLogger(__name__)


# MAIN ACTION TASKS
def getObjective(*args):
    # A main objective task, get objective
    '''
    Meta task
    This is the initial function called when instigating a 
    dialogue between robot and person
    '''
    inVal = raw_input(10*'*'+"What would you like me to do"+10*'*'+'\n')
    InfoBag.Bag["lastUtterance"] = inVal

    logger.debug("GetObjective running:")
    logger.debug(inVal)

    MExObject = MEx.MEx(str(inVal), ["task"])
    value = MExObject.value

    
    returnValue = False
    errMsg = ''

    try : 
        logger.debug("Trying to run value: "+ str(value))
        newTask = static.tasks[value]
        newTask = TaskHandler.TaskHandler.TaskHandler(newTask)
        returnValue, errMsg = newTask.run()
        logger.debug("Finished correctly")

    except :
        logger.info("action.py - ERROR:")
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
    ## WHO
    task = args[0]
    name = ""
    gotName = False
    iterCounter = 1
    while not gotName and iterCounter < 3:
        results = getWho("Who would you like to meet", task)
        gotName = results[0]
        name = results[1]
        # TODO process name results to try to refine name results,
        # i.e. connect to database

        iterCounter += 1
        print("Finished while loop with: {} / {}".format(gotName, name))

    if not gotName:
        return False, "Could not get name of person to meet with"

    ## Where
    ## When 
    
    return True, name

def makeACall():
    pass
## END OF MAIN FUNCTIONS

## SMALL HELPING FUNCTIONS

def getNameForMeeting():
    # A specific vector for timeout to be 
    # processed parallelled   
    # Depricated due to question string not dying
    timeOutVec =  [10, "Getting name"]
    getWhoVec = "Who would you like to meet"

    return dualProcess.dualProcess(timeOut, getWho,
                                   timeOutVec, getWhoVec)


## END OF SMALL HELPING FUNCTIONS


#  *   *   *   SPECIAL FUNCTIONS FOR PARALLELL RUNNING *   *   *
def getWho(*args):
    value  = args
    outStr = value[0]
    task   = value[1]
    print(outStr + '\n')
    i,o,e = select.select([sys.stdin], [], [], int(task.maxDuration))

    if i:
        inStr = sys.stdin.readline().strip()
        #TODO connect inStr to name database and return
        # value

        return True, inStr
    return False, "Found no one - meeting"
    
    
def timeOut(*args):
    args = args[0]
    T = args[0]
    errMsg = args[1]
    time.sleep(T)
    return False, "Timer timeout: "+errMsg


# Definition of callable functions, other functions are 
# called by these functions
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
