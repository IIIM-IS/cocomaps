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

# SPECIFIC TO UNIX SYSTEMS, -FLUSHING INPUT BUFFER
import termios

from Modules import static as static, InfoBag, Timer
import Modules as TaskHandler
# Get MEx form one level up
parentdir = __file__[:-23]
os.sys.path.insert(0,parentdir)
import MEx.MEx as MEx

# Currently assuming this file is the only file to use MEx
# othervise move MEx init to tdm
MEx = MEx.MEx()
logger = logging.getLogger(__name__)


# MAIN ACTION TASKS
def getObjective(*args):
    '''
    Meta task
    This is the initial function called when instigating a 
    dialogue between robot and person
    '''
    while True:
        # Change this line out to get a string input from YTTM
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        inVal = raw_input(10*'*'+"What would you like me to do"+10*'*'+'\n')

        # Store last instance in bag, currently not used however might come
        # in handy later
        InfoBag.Bag["lastUtterance"] = inVal
        logger.info("Input utterance {}".format(inVal))
        # Run the computational instance of the MEx
        values_tuple = MEx.computeWords(inVal)

        # Define template for the objective
        template = ["ScheduleMeeting", "AnswerQuestion", "MakeACall"]
        # Process the template and get the highest possible output
        # when comparing sentance to template
        value = process_template(values_tuple, template)
        if confirm_input(value):
            break
        
    returnValue = False
    errMsg = ''

 #   try : 
    logger.debug("Trying to run value: "+ str(value))
    print "Starting new task {}".format(value)
    newTask = static.tasks[value]
    newTask = TaskHandler.TaskHandler.TaskHandler(newTask)
    returnValue, errMsg = newTask.run()
    logger.debug("Finished correctly")

 #   except :
 #       logger.info("action.py - ERROR:")
 #       logger.info(value)
 #       logger.info(sys.exc_info()[0])

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
    return False, "Unable to greet person"


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

    # ASSUMPTION : We can only get to here if it's through the getObjective 
    # function. Ergo InfoBag.Bag has a previous sentence in its buffer, 
    # This is important because now we can run a who_search
    task = args[0] 
    print("Allright let's schedule a meeting, " + InfoBag.Bag["personName"])

    # Set last utterance to variable to check if names are there
    in_val = InfoBag.Bag["lastUtterance"]
    iterCounter = 0
    contacts = None
    first_run = True
    abort = False
    while True and iterCounter < 5:
        names, possible_names = MEx.search_name(in_val)
        print "debug : 01"
        print names
        print possible_names
        if abort_process(MEx.computeWords(in_val)):
            abort = True
            break

        if first_run :
            first_run = False
        else :
            if not names and not possible_names:
                print("Sorry I don't know them...")
        if names:
            for name in names:
                if contacts:
                    contacts.append(name)
                else :
                    contacts = [name]
        
        if possible_names:
            print("Got the following possible values")
            for name in possible_names:
                 print  "Did you mean {} {}".format(name.first_name, name.last_name)
                 accept = confirm_input("setup a meeting with him/her")
                 if accept:
                     if contacts:
                         contacts.append(name)
                     else :
                         contacts = [name]

        if contacts: 
            print "I am setting up a meeting with"
            for name_item in contacts:
                first_name = name_item.first_name
                last_name = name_item.last_name
                full_name = first_name + ' ' + last_name
                print full_name
            accept = confirm_input("Meeting")

        if contacts:
            print "Would you like to meet with anyone else?"
            accept = confirm_input("Meet someone else")

            if not accept:
                break
            iterCounter -= 1
            in_val = getWho(task,"Who else would you like to meet?")
        else :
            in_val = getWho(task, "Who would you like to meet")

        iterCounter += 1
    if not contacts and not abort:
        print "Sorry unable to schedule a meeting... :()"
        return False, "Unable to setup a meeting"
    elif abort:
        print "User cancelled scheduling a meeting"
        return True, "User aborted"
    else :
        print "Allrighty then, I will setup a meeting with "
        for val in contacts:
            print "{} {} - {}".format(val.first_name, val.last_name, val.email)
        accept = confirm_input("meeting schedule")
        if accept :
            print "Next we will find a timeslot"
            return True, name
        else :
            print "Aborted the meeting"
            return False, "User aborted meeting plan"

def makeACall():
    pass
## END OF MAIN FUNCTIONS

## PROCECCING FUNCTIONS
def confirm_input(name = ""):
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    value = 'deny'
    print "Accept/Deny : {}\n".format(name)
    i,o,e = select.select([sys.stdin], [], [], 20) # set max-time to 10 sek
    logger.info("Asking confirmation for {}".format(name))
    if i:
        inStr = sys.stdin.readline().strip()
        #TODO connect inStr to name database and return
        # value
        logger.info("Got input : {}".format(inStr))
        values_tuple = MEx.computeWords(inStr)
        template = ['accept', 'deny']
        value = process_template(values_tuple, template)
        
    if value == 'accept':
        return True
    return False 

def getWho(*args):
    value  = args
    outStr = value[1]
    task   = value[0]
    print(outStr + '\n')
    # Clear the input buffer
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
    i,o,e = select.select([sys.stdin], [], [], int(task.maxDuration))

    if i:
        inStr = sys.stdin.readline().strip()
        #TODO connect inStr to name database and return
        # value

        return inStr
    return "!"

def abort_process(values_tuple):
    result = process_template(values_tuple, ["abort"])
    if result :
        if confirm_input(" ABORT process"):
            return True
    return False

def process_template(values_tuple, template):
    for value in values_tuple:
        associate   = value[0]
        val         = value[1]

        if associate in template and not val==0:
            return associate
    return None
## END OF PROCESSING FUNCTIONS


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
