#!/usr/bin/python2.7
"""
02.01.18
Author 
    David Orn : david@iiim.is
Objective
    Create a library for all possible actions that can be performed. 
    There are two types of actions. 
                Local   = Happening on the robot in conversation
                Remote  = Happening on the robot in motion
    The action function decides which is which. The context of the action
    should reveal which it should do. 
"""

from timeit import default_timer as timer
import numpy as np
import logging

logger = logging.getLogger("action_lib")

def greet_error():
    """
    Specific error. Gets called by greet function. This means that the 
    system can't greet and there is a huge error and we must restart the entire
    system
    """
    return False


def talk(_dict):
    """
    call_type = Task
    Local action, taking a random string from the out_string field of the input 
    task and throwing it to Nunace to speak.
    """
    n = np.random.randint(0,len(_dict["Task"].out_strings))
    out_str = _dict["Task"].out_strings[n]

    # Send the random string to Nuance
    passed = _dict["NUANCE"].write(out_str)

    return passed, []


def get_input(_dict):
    """
    call_type = Tasks
    Asks based a random question from question list (out_strings), using
    Nuance interface. Nuance stores newest value in word_buffer and returns
    the words. 
    """
    inp = _dict["NUANCE"].read()
    
    return True, dict

def new_task(_dict):
    """
    call_type = Varied
    Return a task name to start given a specific input type, i.e. depending
    on the current task pass_action we can jump to a new task.
    There are two types of new task calls. With keyword reference 
    or with search. I.e. search returns a specific type based on input string
    if type is found. The other returns directly
    """

    # first no keywords, the value is directly set in the pass_action field of
    # the current task
    logger.info("Function call : new_task, from task '{}'".format(_dict["Task"].name))
    task = None
    if not _dict["Task"].keywords:
        logger.info("No keywords in task")
        if _dict["Task"].pass_action:
            task = _dict["MEx"].Types["Tasks"][_dict["Task"].pass_action]
            logger.debug("Found pass_action task : {}".format(task.name))
    else :
        # Keyword search on input value, assumes that there is a sentance in 
        # the word buffer. If no words in buffer of p values empty ask again
        logger.info("Keywords in task")
        if not _dict["NUANCE"].word_buffer:
            talk(_dict)
            get_input(_dict)

        for count in range(_dict["Task"].max_tries):
            # Assuming there is value in the NUANCE buffer, compute the
            # probability of each type
            p = _dict["MEx"].dict_search("Tasks" ,
                                    _dict["Task"].keywords,
                                    _dict["NUANCE"].word_buffer)
            if p.sum() == 0:
                # Unable to detect value in range. Must ask user again 
                # and wait for new input
                talk(_dict)
                get_input(_dict)

            else :
                # If anything was computed, select the highest possible 
                # value, ask user if he accepts the input value.
                index = np.argmax(p)
                task_name = _dict["Task"].keywords[index]
                confirm_string = "Do you want to continue with {}".format(task_ref(task_name))
                _dict["confirm_string"] = confirm_string
                conf_ = confirm(_dict)
                if not conf_ == "Error":
                    if conf_ == True:
                        task =  _dict["MEx"].Types["Tasks"][task_name]
                        break
                    else: 
                        task = None
                        break

    if not task:
        return False, []

    logger.debug("'new_task' returning True and task :{}/ {}".format(
                                                            type(task),
                                                            task.name))
    return True, task

def yes():
    return True, "accepted"
def no():
    return False, "rejected"

def check_abort(_dict):
    """
    call_type = Task
    Assert that the user wants to abort current action.
    """
    pass

def confirm(_dict):
    """
    call_type = Task
    Ask the user to confirm action. 
    """
    _dict["NUANCE"].write(_dict["confirm_string"])
    _dict["NUANCE"].read()
    logger.debug("Asking from confirmation")

    p = _dict["MEx"].dict_search("Tasks", 
                             _dict["MEx"].Types["Tasks"]["confirm"].keywords,
                            _dict["NUANCE"].word_buffer)

    if p.sum() != 0:
        if p[0] > p[1]:
            logger.debug("Permission accepted")
            # Found positive value, return confirm
            return True
        else :
            logger.debug("Permission rejected")
            # By default reject value if no positive found
            return False
    if p.sum == 0:
        logger.info["'confirm' unable to find value in input"]
        return "Error"


def move(_dict):
    # Move can both be called without a location in buffer and with a location
    # in buffer. I.e. ask where to move via task. This function tries
    # to figure out if there are relevant values within the buffer that 
    # indicate which point to move the other robot to
    logger.debug("Started move:")
    p = _dict["MEx"].dict_search("Locations",  _dict["Task"].keywords,
                                            _dict["NUANCE"].word_buffer)
    point = None
    check_again = False
    if p.sum() != 0:
        logger.debug("Found in NUACNE buffer(0), calling: {}".format(_dict["Task"].keywords[np.argmax(p)]))
        point = _dict["MEx"].Types["Locations"][_dict["Task"].keywords[np.argmax(p)]]
        check = confirm_question_string = "Did you select point {}".format(point.name)
        if check != "Error":
            if check == "False":
                check_abort = True
        else:
            check_again = True

    # Else ask user for input.
    if check_again:
        question = "Which point would you like to move to?"
        for i in range(_dict["Task"].max_tries):
            # Ask the question again
            _dict["NUANCE"].write(question)
            # Read the user input
            new_input = _dict["NUANCE"].read()
            #Compare probability
            p = _dict["MEx"].dict_search("Locations",  _dict["Task"].keywords,
                                            _dict["NUANCE"].word_buffer)
            if p.sum() != 0:
                point = _dict["MEx"].Types["Locations"][_dict["Task"].keywords[np.argmax(p)]]
                confirm_question_string = "Did you select point {}".format(point.name)
                _dict["confirm_string"] = confirm_question_string
                check = confirm(_dict)

                if check != "Error":
                    if check == "True":
                        break
                    else :
                        point = None 
                        continue
            else:
                point = None
    

    
    # TODO : Thor, we need to write the objective to psyclone and monitor
    # if the objective has finished
    not_finished = True
    start = timer()
    while not_finished:
        # TODO : Thor check for execution or error
        if timer() - start > _dict["Task"].max_time:
            break

    return True, []


# * * * * * * Functions that are more for show 
def joke(_dict):
    """
    call_type = Task
    Silly function that tells a joke. No specific reason other than to 
    show that the system isn't programmed linearly to solve problems.
    """
    _dict["NUANCE"].write("Why did the robot cross the road? ")
    # Can be implemented 
    inp = _dict["NUANCE"].read()
    _dict["NUANCE"].write("Error 404 page not found")
    return True, []

def ComputerSaysNo(_dict):
    """
    call_type = Task
    Development function to close possible dead ends. It means that the 
    system functionally hasn't been setup in that manner. 
    """
    pass
# * * * * * * * * PASS ACTIONS DEFINITION
def Continue(_dict):
    """
    Positive exit of an objective.
    """
    return True

def RunNextTask(_dict):
    """
    A function call when one task finishes and calles on the next task.
    """
    return True

# * * * * * * * * FAIL ACTIONS DEFINITION

def RetryAction():
    """
    Try to run the objective again. The maximum times an objective is 
    tried is defined in task.max_tries. 
    """
    pass


# * * * * * * * * * CALLER FUNCTION, USED IN TDM
def Action_Call(str_val, _dict):
    """
    Overhead caller, takes in the str value of the task and the task. 
    Maps the str_val to which function should be called.
    [Technical note: The _dictionary method is more compact and pretty, the 
    alternate method is a long if...elif...else, it does handle wrong inputs
    or undefined objectivs. But we want the pretty one]
    input :
            str_val     = name of function to be called (or reference name)
            _dict        = packed _dictionary to send forwareds for any 
                                additional information
    """
    action__dict = {"greet_error":greet_error,
                    "talk":talk,
                    "get_input":get_input,
                    "new_task":new_task,
                    "move":move,
                    "check_abort":check_abort,
                    "confirm":confirm,
                    "joke":joke,
                    "ComputerSaysNo":ComputerSaysNo,
                    "Continue":ComputerSaysNo,
                    "RunNextTask":RunNextTask,
                    "RetryAction":RetryAction}
    # send the information forward to the called function.
    return action__dict[str_val](_dict)


# Dictionary for reference values for output strings
def task_ref(str_name):
    """
    Dictionary that moves a task reference id to a string that the user 
    can understand
    """
    # Return grammatical output: Would you like to continue/abort {} 
    if str_name == "ask_question":
        return "askinging me a question"
    elif str_name == "start_generator":
        return "starting up a generator"
    elif str_name == "tell_joke":
        return "telling you a joke"
