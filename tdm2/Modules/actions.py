# Define all possible action tasks here. Remember that they need to return
# True if they are successful False if they fail, e.g. on time
# Author : david@iiim.is

import time, json, random

global debug
debug = 0


def now():
    return int(round(time.time()*1000))


def elapsed(start):
    curr = now()
    elapsed = curr-start 
    if debug == 1:
        print(elapsed)
    return elapsed 


def getRightQuestion(id):
    # Based on a question ID search the database,
    dictionary = {}
    with open('questions', 'r') as fobj:
        dictionary = json.load(fobj)
    selected = dictionary[id]
    # Randomly return one of the strings availible
    return selected[random.randrange(len(selected))]
    

def sayQuestion(text):
    # Send text to interpreter and say it outlout
    # TODO connect to sound out parser
    #       - Create a timeout approach based on 
    #           input line length
    #       - Create an interrupt approach
    # 
    # DEBUG
    errStr = "actions:sayQuestion - Interrupted during question"
    print text
    return True, errStr


def getInput(questionID):
    # Fill out a template, fill out global bag with relevant values
    # the template is connected to the questionID aka name of 
    # task.

    # TODO 
    #   Create template dictionary
    #   Create global bag with information
    #   Create function for each question tasks, based on name

    if questionID == "AskForInput":
        # Set debug mode on
        getTask = raw_input("DEBUG INPUT: ")
        if getTask == "call":
            None # This test ensures that the new task
                 # is in fact a task
        else :
            return False, ""

        return True, getTask


def askQuestion(timeOut, questionID):
    # Ask the user a question, questions are different based on 
    # questionID: which defines where the question comes from and
    # therefore what is should be.
    # TODO : 
    #       - Interrupter
 
    questionStr = getRightQuestion(questionID)

    start = now
    # TODO send question to text-to-speach converter..
    test, errStr = sayQuestion(questionID)
    if not test: # Interrupted during asking question
        return False, errStr
    return getInput(questionID) # Save input to template defined by quesitonID

    if elapsed(start) > timeOut:
        return False
    return True, ""


def HeadMove(timeOut, direction):
    now_ = now()
    # Todo -> If we max timeout we should have a function call : e.g.
    # clear buffer or go to tree. [Perhaps returning false will do]
    if direction == "HeadTurnLeft":
        if debug == 1:
            print("Debug : moving head left")
            time.sleep(.5)
        if elapsed(now_) > timeOut:
            errStr = "Failed: action>HeadMove->HaedTurnLeft"
            return False, errStr

    elif direction == "HeadTurnRight":
        if debug == 1:
            print("Debug: Moving head right")
            time.sleep(.5)
            print(str(elapsed(now_))+ ">" + str(timeOut))
        if elapsed(now_) > timeOut:
            errStr = "Failed: action>HeadMove->HaedTurnRight"
            return False, errStr
        

    elif direction == "HeadFacingForward":
        if debug == 1:
            print("Debug: Facing head forwards")
            time.sleep(.5)
        if elapsed(now_) > timeOut: 
               errStr = "Failed: action>HeadMove->HaedTurnRight"
               return False, errStr
       
    return True, ""

    
if __name__=="__main__":
    print(getRightQuestion("Greeting"))
