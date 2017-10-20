# A function dictionary, here new actions can be implimented
# added to the dictionary and called instantly

import InfoBag

def askMeAnything(*args):
    '''
    NOT IMPLEMENTED
    This function starts a subprogram allowing for input of question
    through voice and output of answer through audio
    Author : david@iiim.is
    '''
    inVal = raw_input("What would you like to know")
    return True, "actions.askMeAnything not implemented"

def askWhoToMeet(*args):
    # Qestion when setting up a meeting, who to meet
    '''
    NOT IMPLIMENTEe
    Action related to setting up a meeting, ask the user for input
    and decide who the user wants to call
    Author : david@iiim.is
    '''
    inVal = raw_input("Who would you like to meet")

    return True, "actions:askWhoToMeet not implemented"

def callSomeone(*args):
    # Function of task make a call - who to call
    '''
    NOT IMPLEMENTED
    Meta task
    Action related to making a call, this starts the subroutine,
    a new task tree, of trying to call someone. 
    Author : david@iiim.is
    '''
    print("META FUNCTIO : Start process of calling someone")

    return True, "actions:callSomeone not implemented"

def getObjective(*args):
    # A main objective task, get input objective
    '''
    NOT IMPLEMENTED
    Meta task
    This is the initial function called when instigating a 
    dialogue between robot and person
    Author : david@iiim.is
    '''
    inVal = raw_input("What would you like me to do")
    return True, "actions:getObjective not implemeted"

def greetPerson(*args):
    # An action where robot greets person
    '''
    NOT IMPLEMENTED
    This task is run when a person has been identified
    it greets person
    Author : david@iiim.is
    '''
    if not InfoBag.Bag["haveGreeted"]:
        print("Good morning kind person")
        InfoBag.Bag["haveGreeted"] = True
        return True, "DEBUG : FINISHED GREETING"
    #iInfoBag.Bag["haveGreeted"] = True
    return False, "actions:greetPerson not implemented"

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

def whenToMeet(*args):
    '''
    NOT IMPLEMENTED
    Part of scheduling a meeting, deciding when to meet. 
    Author : david@iiim.is
    '''
    # Ask for input, time: when to schedule meeting
    inVal = raw_input("When would you like to meet")

    return True, "actions:whenToMeet not implemented"

def whereToMeet(*args):
    '''
    NOT IMPLEMENTED
    Part of scheduling a meeting, set location of meeeting
    Author : david@iiim.is
    '''
    # Scheduling meeting, where should the meeting take 
    # place
    inVal = raw_input("Where would you like to meet")
    return True, "actions:whereToMeet not implemented"

def whoToCall(*args):
    '''
    NOT IMPLEMENTED
    Part of making a callSomeone, decides whom to call and 
    makes call
    Author : david@iiim.is
    '''
    # Scheduling a call, whom to call
    inVal = raw_input("Who should robot call")
    return True, "actions:whoToCall not implemented"



actions = {
    "askMeAnything" : askMeAnything,
    "askWhoToMeet"  : askWhoToMeet,
    "callSomeone"   : callSomeone,
    "getObjective"  : getObjective,
    "greetPerson"   : greetPerson,
    "headTurn"      : headTurn, 
    "whenToMeet"    : whenToMeet,
    "whereToMeet"   : whereToMeet,
    "whoToCall"     : whoToCall
}



class debugClass():
    def __init__(self, name):
        self.name = name


if __name__ == "__main__":
    task1= debugClass("TurnLeft")
    task2= debugClass("TurnRight")
    task3= debugClass("FaceForwards")
    for key in actions.keys():
        if key == "headTurn":
            actions[key](task1)
            actions[key](task2)
            actions[key](task3)
        else : 
            actions[key]()

