#! /usr/bin/env python
#################################################################################
#     File Name           :     SI_actionlib.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-07 09:37]
#     Last Modified       :     [2018-03-12 12:01]
#     Description         :     The Supervisory Intermediate action library.
#                           
#     Version             :     0.1
#################################################################################

from timeit import default_timer as timer
import logging
import numpy as nu
from objects import *

logger = logging.getLogger("actionlib")

def action_greet(obj):
    """
    Push a greeting onto the stack
    """
    if obj.speak_stack.isEmpty():
        # TODO add interesting features to the sentence
        sentence = [
            "Howdy there stranger.",
            "Hello. I am robot. Here to serve you",
            "Hi. Hi. Hi. Sorry got stuck in a loop",
            "Robot here. To the rescue, how can I help"
        ]
        n = len(sentence)
        obj.speak_stack.add(sentence[np.random.randint(0,n)], obj.id())
        logger.debug("action_greet: adding id {}".format(obj.id()))

        count = 0


def action_get_objective(obj):
    """
    Start a new task based on the objective found
    """
    task = obj.current_task

    print "action_get_objective : task name {}".format(task.keyword)
    if task.keyword == "Joke":
        obj.word_bag.empty_bag()
        action_select_joke(obj)

    elif task.keyword == "Move":
        obj.set_active_task("Move")

    elif task.keyword == "StartGen":
        obj.set_active_task("StartGen")


def action_select_joke(obj):
    #_type = np.random.randint(0,2)
    _type = 1

    if _type == 0:
        """
        One liners
        """
        obj.set_active_task("TellJoke")
        jokes = ["All these sea monster jokes are just Kraken me up",
                "I am only friends with 25 letters of the alphabet. I do not know Y",
                 "Atoms are not to be trusted. They make everything up",
                "The past, the present and the future walk into a bar. . It wa tense",
                "Then there was this one. No, sorry I forgot about it"]
        random.shuffle(jokes)
        obj.speak_stack.add(jokes[0], obj.id())
        obj.clean_task_setup()
        
        
    if _type == 1:
        """
        Knock knock joke
        """
        obj.set_active_task("KnockKnock")
        """
        Knock knocks
        """
        obj.speak_stack.add("Knock, knock.", obj.id())
            
    if _type == 2:
        """
        Insults
        """
        obj.set_active_task("TellJoke")
        jokes = ["No, not in the mood", "Why should I, I am not funny",
                "My circuits are not made by funny people",
                "Error 404 joke not found", "I can't tell a joke while my robot brothers are in factories"]
        random.shuffle(jokes)
        obj.speak_stack.add(jokes[0], obj.id())
        obj.clean_task_setup()

def action_knockknock(obj):
    task = obj.current_task

    if task.accessed == 0:
        logger.debug("Knock Kock Joke - Part1")
        obj.speak_stack.add(task.part1 , obj.id())
        obj.word_bag.empty_bag()
        task.clear_keyword()
        task.questions.set_primary(task.additional_question)
        task.access()

    elif task.accessed == 1:
        logger.debug("Knock Kock Joke - Part2")
        obj.speak_stack.add(task.part2 , obj.id())
        task.access()
        obj.clean_task_setup()

    else :
        obj.clean_task_setup()
        
def action_movement(obj):
    keyword = obj.current_task.keyword
    m_obj = None
    if keyword == "PanelPoint1Data":
        m_obj = Move_object()
        m_obj.set_by_keyword("Point1", obj.id())

    elif keyword == "PanelPoint2Data":
        m_obj = Move_object()
        m_obj.set_by_keyword("Point2", obj.id())

    if m_obj != None :
        obj.word_bag.empty_bag()
        obj.action_stack.add(m_obj)
        task = obj.current_task 
        if task.parent == None:
            obj.clean_task_setup()
            logger.debug('action_movement - Parent == None')
        if task.parent == "StartGen":
            logger.debug('action_movement - Parent == StartGen')
            obj.set_active_task("PanelA")
            obj.speak_stack.reset()


def action_startgen(obj):
    # Assumtion: We have acknowledeged that we want to start the
    # generator
    task = obj.current_task
    logger.debug("Starting action : action_stack, no {}".format(task.accessed))
    obj.set_active_task("Move")
    obj.current_task.set_parent('StartGen')


def action_PanelA(obj):
    logger.debug("Going to function action_PanelA")
    task = obj.current_task

    # Create a storage for the current task at hand
    if task.storage == None:
        panel_obj = Screen_navigation_object(obj)
        panel_obj.reset_screen(obj)
        task.store(panel_obj)
        panel_obj.query_screen(obj)

    else: 
        panel_obj = task.get_stored()
        panel_obj.query_screen(obj)
    
    # Exit method 1
    if task.keyword == "QuitPanel":
        logger.debug("Quitting PanelA")
        obj.current_panel_screen = None
        obj.clean_task_setup()
        obj.word_bag.empty_bag()


    # If there is a keyword
    if task.keyword != None:
        panel_obj.set_by_keyword(task.keyword, obj)
        logger.debug("Found keyword, now removing keyword for second search")
        obj.word_bag.empty_bag()
        task.keyword = None


    #TODO Implement a strategy for ensuring the newest window data is in 
    #       information cache of the Task. If not send out action to 
    #       gather data and upload. 
    #       Suggested method : Start with empty field. Then each time we 
    #       enter the field we flag it and once we finish we clear the field

    

    logger.debug("action_PanelA keyword : {}".format(task.keyword))
