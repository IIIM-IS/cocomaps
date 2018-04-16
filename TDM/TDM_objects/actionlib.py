#! /usr/bin/env python
#################################################################################
#     File Name           :     SI_actionlib.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-07 09:37]
#     Last Modified       :     [2018-03-28 15:30]
#     Description         :     The Supervisory Intermediate action library.
#
#     Version             :     0.1
#################################################################################

from timeit import default_timer as timer
import logging
import numpy as nu
from objects import *

logger = logging.getLogger("actionlib")

def delay(t):
    now = timer()
    while timer()-now < t:
        pass

def passive(obj):
    logger.debug("#TDM: Passive State Active")

def action_greet(obj):
    """
    Push a greeting onto the stack
    """
    if obj.speak_stack.isEmpty():
        # TODO add interesting features to the sentence
        sentence = [
            "Hello. Please wait while I boot systems"
        ]
        n = len(sentence)
        obj.speak_stack.add(sentence[np.random.randint(0,n)], obj)
        logger.debug("#TDM: action_greet: adding id {}".format(obj.id()))

        count = 0


def action_get_objective(obj):
    """
    Start a new task based on the objective found
    """
    task = obj.current_task
    obj.speak_stack.reset()
    obj.asked_first_reset()

    if task.keyword == "Joke":
        obj.word_bag.empty_bag()
        action_select_joke(obj)
        task.finished()

    elif task.keyword == "Move":
        obj.set_active_task("Move")
        task.finished()

    elif task.keyword == "StartGen":
        obj.set_active_task("StartGen")
        task.finished()

    elif task.keyword == "Screen":
        obj.set_active_task("PanelA")
        action_PanelA(obj)

def randi():
    return np.random.randint(0,3)

def action_select_joke(obj):
    _type = np.random.randint(0,2)
    obj.asked_first_reset()

    if _type == 0:

        """
        One liners
        """
        obj.set_active_task("TellJoke")
        jokes = ["All these sea monster jokes are just, Kraken me up",
                "I am only friends with 25 letters of the alphabet. I don't  know Y",
                 "Atoms are not to be trusted. They make everything up",
                "The past, the present and the future walk into a bar. . It was tense",
                "Then there was the one about. . . No, sorry I forgot about it"]
        obj.speak_stack.add(jokes[randi()], obj)
        obj.clean_task_setup()

    if _type == 1:
        """
        Insults
        """
        obj.set_active_task("TellJoke")
        jokes = ["No, not in the mood", "Why should I, I am not funny",
                "My circuits are not made by funny people",
                "Error 404 joke not found", "I can't tell a joke while my robot brothers are in factories"]
        obj.speak_stack.add(jokes[randi()], obj)
        obj.clean_task_setup()


def action_knockknock(obj):
    task = obj.current_task

    if task.accessed == 0:
        logger.debug("#TDM: Knock Kock Joke - Part1")
        obj.speak_stack.reset()
        obj.speak_stack.add(task.part1 , obj)
        obj.word_bag.empty_bag()
        task.clear_keyword()
        task.questions.set_primary(task.additional_question)
        task.access()

    elif task.accessed == 1:
        logger.debug("#TDM: Knock Kock Joke - Part2")
        obj.speak_stack.reset()
        obj.speak_stack.add(task.part2 , obj)
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
    task = obj.current_task
    if task.keyword != None:
        move_obj = Move_object()
        logger.debug("#TDM action_startgen : move to {}".format(task.keyword))
        id = obj.id()
        if task.keyword == "PanelPoint1Data":
            move_obj.set_by_keyword("Point1", id)
        elif task.keyword == "PanelPoint2Data":
            move_obj.set_by_keyword("Point2", id)

        obj.action_stack.add(move_obj)

        start = timer()

        obj.set_active_task("PanelA")
#       action_PanelA(obj)


def action_PanelA(obj):
    logger.debug("#TDM: Going to function action_PanelA")
    task = obj.current_task
    # Create a storage for the current task at hand
    if obj.get_storage() == None or obj.get_storage().type != "Panel":
        logger.debug("Creating panel nav object")
        panel_obj = Screen_navigation_object()
# <16.04.18> Try removing, technically it shouldn't be needed.
#        panel_obj.reset_screen(obj)
        obj.set_storage(panel_obj)
        obj.word_bag.empty_bag()
    else:
        logger.debug("Loading panel nav object")
        panel_obj = obj.get_storage()
        panel_obj.query_screen(obj)
        obj.word_bag.empty_bag()
    logger.debug("Window panel screen name : {}".format(panel_obj.screen_name))
    # Handle the creation of a new task to solve panel navigation
    if panel_obj.screen_name != None:
        if panel_obj.screen_name == "main":
            obj.set_active_task("screen_main")
        elif panel_obj.screen_name == "power_up":
            obj.set_active_task("screen_power_up")
        elif panel_obj.screen_name == "power_down":
            obj.set_active_task("screen_power_down")
        elif panel_obj.screen_name == "status":
            obj.set_active_task("screen_status")
# Special case, the pin number
        elif "_pin" in  panel_obj.screen_name:
            obj.set_active_task("screen_pin")
            action_panel_pin(obj)
# Catch all possible types, if type not handled assume main menu
    else:
        obj.set_active_task("screen_main")

def action_panel_pin(obj):
    # If storage is empty create a new pin search object
    logger.debug("#TDM ActionPin {}".format(obj.get_storage().type))
    if obj.get_storage() is None or obj.get_storage().type != "PinQuery":
        logger.debug("#TDM: First pin query")
        pin_obj = Pin_Query()
        obj.set_storage(pin_obj)
    # If something is in the storage then it is a pin search
    # object. Continue the search for a pin
    else:
        pin_obj = obj.get_storage()
        logger.debug("#TDM: Pin query")

    if pin_obj.queueing():
        logger.debug("#TDM : Pin in queue")
        # Check if the value has returned passed i.e. good or
        # if the entered pin failed
        # passed, value  =  MEx.pin_search(word_bag)

        if pin_obj.passed:
            pass
            # Handled in the outer region
        else:
            if obj.CONTENT_INTERPRETED:
                obj.not_asked()
                obj.set_active_task("PanelA")
                obj.set_storage(None)
    else:
        # Check if user said quit or stop searching
        p = obj.MEx.dict_search(["QuitPanel"],
                                obj.word_bag)
        if p.sum() > 0:
            obj.set_active_task("PanelA")
            obj.set_storage(None)
        else:
            # Check if the pin is in the word bag, if so send pin to
            # panel and wait for confirmation/negation
            passed, val = obj.MEx.pin_search(obj.word_bag)
            if passed:
                # Send pin to panel for evaluation
                obj.speak_stack.reset()
# <16.04.18> To fast, pin gets processed much faster than computer
# tells it... need to fix?
#                out_str = "Trying pin number: {}".format(val)
#                obj.speak_stack.add(out_str, obj)
                pin_obj.add(val, obj)
                obj.word_bag.empty_bag()
            else:
                if not obj.check_asked():
                    obj.speak_stack.reset()
                    obj.speak_stack.add("What pin should we try", obj)
                    obj.set_CI(False)




def action_panel_navigate(obj):
    # You get here on a new panel task
    screen_name = obj.current_task.name
    keyword = obj.current_task.keyword
    logger.debug("action_panel_navigate : keyword= {}".format(keyword))
    if keyword is not None:
        # Retrieveg a push button object
        screen_nav_obj = obj.get_storage()
        logger.debug('#TDM: action_panel_navigate :Screen {}'
                     '-Keyword {}'.format(screen_name, keyword))
        # * * * * * * * * Main screen * * * * * * * * * * * * * *
        if screen_name == "screen_main":
            if keyword == "Button1":
                screen_nav_obj.push_button("power_up", obj)
                obj.set_active_task("screen_pin")
            elif keyword == "Button2":
                screen_nav_obj.push_button("power_down", obj)
                obj.set_active_task("screen_1pin")
            elif keyword == "Button3":
                screen_nav_obj.push_button("status", obj)
                obj.set_task_by_reference(obj)
                obj.set_active_task("PanelA")
            elif keyword == "Back":
                screen_nav_obj.back_button(obj)
                obj.set_active_task("PanelA")
            elif keyword == "NoButton":
                screen_nav_obj.push_button("no_button", obj)
                obj.set_active_task("PanelA")
            elif keyword == "Home":
                screen_nav_obj.reset_screen(obj)
                obj.set_active_task("PanelA")
            elif keyword == "Abort":
                obj.set_active_task("GetObjective")
                obj.set_storage(None)
            elif keyword == "QuitPanel":
                obj.set_active_task("StartGen")
                obj.set_storage(None)

        # * * * * * * * * Power up screen * * * * * * * * * * * * * *
        elif screen_name == "power_up":
            if keyword == "Button1":
                screen_nav_obj.push_button("confirm_power_up", obj)
                obj.set_active_task("PanelA")
            elif keyword == "Button2":
                screen_nav_obj.push_button("cancel_power_up", obj)
                obj.set_active_task("PanelA")
            elif keyword == "NoButton":
                screen_nav_obj.push_button("no_button", obj)
                obj.set_active_task("PanelA")
            elif keyword == "Back":
                screen_nav_obj.back_button(obj)
                obj.set_active_task("PanelA")
            elif keyword == "Home":
                screen_nav_obj.reset_screen(obj)
                obj.set_active_task("PanelA")
            elif keyword == "Abort":
                obj.set_active_task("GetObjective")
                obj.set_storage(None)
            elif keyword == "QuitPanel":
                obj.set_active_task("StartGen")
                obj.set_storage(None)

        # * * * * * * * * Power down screen * * * * * * * * * * * * * *
        elif screen_name == "power_down":
            if keyword == "Button1":
                screen_nav_obj.push_button("confirm_power_down", obj)
                obj.set_active_task("PanelA")
            elif keyword == "Button2":
                screen_nav_obj.push_button("cancel_power_down", obj)
                obj.set_active_task("PanelA")
            elif keyword == "Back":
                screen_nav_obj.back_button(obj)
                obj.set_active_task("PanelA")
            elif keyword == "NoButton":
                screen_nav_obj.push_button("no_button", obj)
                obj.set_active_task("PanelA")
            elif keyword == "Home":
                screen_nav_obj.reset_screen(obj)
                obj.set_active_task("PanelA")
            elif keyword == "Abort":
                obj.set_active_task("GetObjective")
                obj.set_storage(None)
            elif keyword == "QuitPanel":
                obj.set_active_task("StartGen")
                obj.set_storage(None)

        # * * * * * * * * Screen Status * * * * * * * * * *
        elif screen_name == "status":
            if keyword == "NoButton":
                screen_nav_obj.push_button("no_button", obj)
                obj.set_active_task("PanelA")
            elif keyword == "Home":
                screen_nav_obj.reset_screen(obj)
                obj.set_active_task("PanelA")
            elif keyword == "Back":
                screen_nav_obj.back_button(obj)
                obj.set_active_task("PanelA")
            elif keyword == "Abort":
                obj.set_active_task("GetObjective")
                obj.set_storage(None)
            elif keyword == "QuitPanel":
                obj.set_active_task("StartGen")
                obj.set_storage(None)

        obj. word_bag.empty_bag()


def action_demo2(obj):
    task = obj.current_task
    if task.keyword != None:
        if task.keyword == "Yes":
            obj.speak_stack.add("Great", obj)
            obj.set_active_task("Start_gen_demo2")
        elif task.keyword == "No":
            obj.speak_stack.add("I will search for someone who can help", obj)
            obj.set_active_task("EmptyState")

        obj.word_bag.empty_bag()


def action_startgen_demo2(obj):
    task = obj.current_task
    if task.keyword is not None:
        move_obj = Move_object()
        logger.debug("#TDM : move : {}".format(task.keyword))
        if task.keyword == "PanelPoint1Data":
            move_obj.set_by_keyword("Point1", obj.id())
        elif task.keyword == "PanelPoint2Data":
            move_obj.set_by_keyword("Point2", obj.id())
        # Force the active action into motion so the system can't
        # continue until it finishes
        obj.action_stack.add(move_obj)

        while obj.active_actions.instack(id):
            count += 1
        obj.set_active_task("Demo2_question")
        obj.word_bag.empty_bag()
        # Demo sepcific dialog
        obj.speak_stack.add("Robot at location. . We could shut down generator 1. Is that okay", obj)

def action_demo2_question(obj):
    task = obj.current_task

    if task.keyword != None:
        # The question is do you want me to turn off the value
        if task.keyword == "Yes":
            panel_obj = Screen_navigation_object()
            panel_obj.reset_screen(obj)
            panel_obj.query_screen(obj)
            panel_obj.push_button("generator_1", obj)
            # Project specific output
            obj.set_active_task("EmptyState")
            obj.speak_stack.add("Ok. Generator 1 has been shut down", obj)
            obj.speak_stack.add("Thank you for your help", obj)
        elif task.keyword == "No":
            obj.set_active_task("PanelB")
        obj.word_bag.empty_bag()

def action_PanelB(obj):
    logger.debug("#TDM: Going to function action_PanelB")
    task = obj.current_task
    # Make the assumption that the current screen is main and
    # it has three buttons
    # Button1
    # Button2
    # Button3
    # Create a storage for the current task at hand
    if obj.get_storage() == None:
        panel_obj = Screen_navigation_object()
        panel_obj.reset_screen(obj)
        obj.set_storage(panel_obj)
        obj.word_bag.empty_bag()
    else:
        panel_obj = obj.get_storage()
        panel_obj.query_screen(obj)

    # We just need a keyword search
    if task.keyword != None:
        obj.word_bag.empty_bag()
        if task.keyword == "B1":
            panel_obj.push_button("gen1", obj)
            obj.speak_stack.reset()
            obj.speak_stack.add("Ok. Generator 1 has been shut down", obj)
        if task.keyword == "B2":
            panel_obj.push_button("gen2", obj)
            obj.speak_stack.reset()
            obj.speak_stack.add("Ok. Generator 2 has been shut down", obj)
        if task.keyword == "B3":
            panel_obj.push_button("gen3", obj)
            obj.speak_stack.reset()
            obj.speak_stack.add("Ok. Generator 3 has been shut down", obj)

        # Object specific output
        obj.set_storage(None)
        obj.set_active_task("EmptyState")
1
