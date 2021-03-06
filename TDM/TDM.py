#! /usr/bin/env python
#################################################################################
#     File Name           :     TDM.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-06 15:12]
#     Last Modified       :     [2018-04-03 10:00]
#     Description         :     Supervisory Intermediate (TDM) control function
#                               takes care of higher level functionality and
#                               feedbacks to the TDM. Becomes the actual
#                               connector with psyclone
#     Version             :     0.1
#################################################################################

from timeit import default_timer as timer
import logging
import tdm_logger
import numpy as np

from TDM_objects.algorithms import TDM_AS
from TDM_objects.algorithms import TDM_AA
from TDM_objects.algorithms import TDM_SS

from TDM_objects.objects import Dialog
from TDM_objects.objects import Word_Bag
from TDM_objects.Tasks import Task_object

from MEx import MEx

class TDM(object):
    """
    Supervisory Intermediate. High level control and response of the
    TDM overall system. Checks inputs/outputs, ensures taks are in correct
    order and that timouts, where required, are mainained.
    Also an upper level control loop, e.g. for inserting the control
    to panel (in a ping-pong push-pull back-forth relationship)
    """
    def __init__(self):
        # Initiate the logging sequence
        tdm_logger.setup_logging()

        # Set the demo method
        self.demo = 3
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting Supervisory Intermediate")
        self.last_action = 0
        self.active = False
        self.dialog = Dialog()
        self.system_id = None

        # Dynamic variables
        self.talk = False
        self.stop = False
        self.last_speak = 0
        self.current_task = None
        self.active_actions = TDM_AA()
        self.action_stack = TDM_AS(self.active_actions)
        self.speak_stack = TDM_SS()
        self.word_bag = Word_Bag()
        self.id_number = 0
        self.asked_first = 0
        self.go_to_search = False
        self.speaking_timeout = 0
        self.word_bag_enabled = True
        self.SESSION_IN_PROGRESS = False
        self.asked = False
        # A panel interaction specific variable. Is given value when
        # system is in interaction with a panel. Otherwise it's none
        self.current_panel_screen = None
        # Storage for various temporary values.
        self.storage = None
        self.previous_task = None
        # Update < 11 Ap 18 >
        # Global variables for system
        self.CONTENT_INTERPRETED = False
        self.CONTENT_UNDERSTOOD = False

        # Static variables:
            # How many times, in a row, can the system ask the user what
            # task to solve before the system stops
        self.max_ask_first = 100
        self.Tasks = Task_object()
        self.MEx = MEx.MEx(self.Tasks)


    def is_active(self):
        return self.active
    # Turn on the session flag, with it on the system, theoretically,
    # moves into present tense methods.
    # TODO :Propagate throught code ??? [Don't know how]
    def SET_SESSION(self):
        self.SESSION_IN_PROGRESS = True

    def asked_first_inc(self):
        self.asked_first += 1

    def asked_first_reset(self):
        self.asked_first = 0

    def turn_on(self):
        self.active = True

    def set_CI(self, val):
        self.CONTENT_INTERPRETED = val

    def set_CU(self, val):
        self.CONTENT_UNDERSTOOD = val

    def not_asked(self):
        """
        <12.04.18>
        C.hange the flag, have I asked the question
        to False, i.e. I have not asked a question
        but would like to.
        """
        self.asked = False

    def check_asked(self):
        # Check if a new question, added to the output string
        # has been asked
        return self.asked

    def finished_asking(self):
        self.asked = True

    def turn_off(self):
        self.current_task = None
        self.action_stack.reset()
        self.word_bag.empty_bag()
        self.active_actions.reset()
        self.go_to_search = True
        self.SESSION_IN_PROGRESS = False

    def reset(self):
        self.active = False
        # Dynamic variables
        self.talk = False
        self.stop = False
        self.last_speak = 0
        self.current_task = None
        self.active_actions.reset()
        self.action_stack.reset()
        self.speak_stack.reset()
        self.word_bag.empty_bag()
        self.id_number = 0
        self.asked_first = 0
        self.go_to_search = False

    def set_system_id(self, id):
        self.system_id = id

    def robot_start_speaking(self, id):
        if self.system_id == id:
            self.word_bag_enabled = False

    def robot_stopped_speaking(self, id):
        if self.system_id == id:
            self.word_bag_enabled = True

    def set_storage(self, obj):
        self.storage = obj

    def get_storage(self):
        return self.storage

    def return_pass(self):
        # Special function for setting active object in storage to
        # true
        if self.get_storage() != None:
            # Sets the input type to passed to let the system know
            # that a value has been accepted
            self.get_storage().return_passed()

    def return_fail(self):
        # Same as return pass except here we set the objective to
        # failed. Handled in actionlib
        if self.get_storage() != None:
            self.get_storage().return_fail()

    def get_speak_stack(self):
        """
        For the TDM_psyclonce call, if there is anything on the speak
        stack return it and pop the stack
        """
        #self.logger.debug("#TDM: Checking speak stack")
        if (not self.speak_stack.isEmpty()
           and not self.active_actions.wait()):
            return self.speak_stack.pop()
            #<12.04.18> Simplified, always return a value if one is
            # available
#            if self.active_actions.wait():
#                out_speak = self.speak_stack.pop(level=1)
#            else :
#                out_speak = self.speak_stack.pop()
#                self.set_speek_timeout(out_speak.max_time)
        # If nothing on the stack return None
        return None

    def set_keywords(self, key, list):
        if self.current_task != None:
            self.current_task.keywords = {key, list}

    def id(self):
        self.id_number+=1
        return self.id_number-1

    # <12.04.18> Need a better way of stopping the system when
    # something is on the action stacks.
    def wait_on_action(self):
        if not self.action_stack.isEmpty():
            for action in self.action_stack.stack:
                if action.get_holds():
                    return True
        if not self.active_actions.isEmpty():
            for action in self.active_actions.stack:
                if action.get_holds():
                    return True
        return False

    def speak_timeout(self):
        """
        Timout period between speaking
        """
        if self.speaking_timeout == 0:
            return True
        if timer() - self.speak_start > self.speaking_timeout:
            return True
        return False

    def set_speek_timeout(self, time):
        self.speak_start = timer()
        self.speaking_timeout = time

    def check_action_stack(self):
        """
        Check if the action stack has anything to offer
        """
        if self.active and not self.action_stack.isEmpty() and not self.active_actions.wait():
            # NOTE : the last statement has implications. We can't enact issues
            # while other issues are in action
            data = self.action_stack.pop()
            return data
        return None

    def clean_task_setup(self):
        """
        Set the system to a default state, clean action stack, speak stack
        and make the current task == None
        """
        self.current_task = None

    def check_task(self):
        """
        Checks that there is an action on the stack. If not add get objective
        task to the stack
        """
        if self.demo == 2:
            if self.current_task == None:
                self.set_active_task("Demo2")
                #self.set_active_task("Demo2_question")

        else:
            if self.current_task == None:
                """ <11 Apr 18> Go straight to how can I help, other
                method is depricated
                # First run, greet is has not been added
                if self.action_stack.history == []:
                    self.logger.debug("#TDM: Adding Greet to stack")
                    self.set_active_task("Greet")
                    self.action_stack.history.append("greet")
                # All other runs, greet is finished. We go straight to
                # get objective
                """
                self.logger.debug("#TDM: Adding GetObjective to stack")
                self.set_active_task("GetObjective")

    def set_task_by_reference(self, task):
        self.current_task = task

    def set_window_by_reference(self, window_name):
        # TODO Add functionality for demo3
        # # # # # # # # # # DEMO 2 # # # # # # # # # # # # # #
        if window_name == "main":
            task_name = "PanelA"
        elif window_name == "power_up":
            task_name = "screen_power_up"
        elif window_name == "power_down":
            task_name = "screen_power_down"
        elif window_name == "status":
            task_name = "screen_power_up"
        elif window_name == "PINCode":
            task_name = "screen_pin"
        else:
            task_name = "PanelA"

        # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        self.set_active_task(task_name)

    def set_active_task(self, task_name):
        """
        Set the current task according to task name. Prepare the
        action stack and check if information is available. If
        not create an speak_object and add on stack. If data is
        available put action_object on action stack
        """
        if self.current_task != None:
            self.previous_task = self.current_task.name
        else:
            self.previous_task = "GetObjective"
        self.logger.debug("New Object : {}".format(task_name))
        new_task = self.Tasks.get(task_name)
        self.asked = False
        self.set_CI(False)
        self.set_CU(False)
        self.current_task = new_task


    def information_query(self):
        """
        Check if there is information in the speak buffer to decide
        what is missing from the task, if not put question on Speach
        Stack
        """
        self.logger.debug("##MEX evaluation")
        task = self.current_task
        if self.current_task != None and self.current_task.keyword == None:
            if self.current_task.name == "GetObjective":
                self.asked_first_inc()
            p = self.MEx.dict_search(task.keywords, self.word_bag)
            if p.sum() == 0:
                if self.asked is False:
                    self.speak_stack.add(task.primary_question(), self)
            else:
                self.logger.debug("#TDM: Current task: {}".format(task.name))
                self.logger.debug("#TDM: Current keywords: {}".format(task.keywords))
                self.logger.debug("#TDM: Current p: {}".format(p))
                self.logger.debug("#TDM: argmax {}".format(np.argmax(p)))
                self.logger.debug("#TDM: Keyword: {}".format(task.keylist[np.argmax(p)]))
                self.set_CU(True)
                task.set_keyword(task.keylist[np.argmax(p)])

            self.set_CI(True)



    def add_to_word_bag(self, sentence):
        """
        Try to add the Nunace input to the word bag.
        """
        # Change the value of having Interpreted the content
        self.set_CI(False)
        self.word_bag.add(sentence)
        self.information_query()

    def silent_run(self):
        """
        Silent run gets checked each time, this pushes actions to action stack
        and ensures that enqueued text is ready

        Can return actions to be performed that don't require timed inputs
        from the user
        """
        # Ensure that there is something active, and that the dialog
        # isn't turned off
        if self is not None and self.active and not self.turn_dialog_off():
            if self.active_actions.wait():
                # Check the active action stack if there are any actions
                # that require a wait period
                None
            elif self.active_actions.timeouts():
                # Check if anything in the active action has a timeout
                # First approach, reset system
                # Identify which task is timed out
                self.logger.info("#TDM Task timeout")
                for idx, action in enumerate(self.active_actions.stack):
                    if action.timeout_check():
                        self.active_actions.pop(id=idx)
                        break
                self.set_active_task(self.previous_task)

            else:
                # No wait periods and no timeouts found. General approach
                if(self.action_stack.isEmpty()
                   and self.speak_stack.isEmpty()):
                    # Not a good method, first that came to mind.
                    if(self.current_task is not None
                       and self.current_task.keyword == "Nothing"):
                        pass
                    else:
                        self.check_task()

                # If the current wordbag content hasn't been interpreted
                # Check for information
                if not self.CONTENT_INTERPRETED:
                        self.information_query()
                # If there is a task active, and the keyword has
                # been set, or if the keyword is set to Nothing
                if(self.current_task is not None
                   and self.current_task.keyword is not None):
                    self.current_task.eval(self)


    def turn_dialog_off(self):
        """
        Check when last input was recorded, if to long. Force dialog off
        """
        if self.max_ask_first - self.asked_first <= 0:
            self.action_stack.history = []
            self.active = False
            return True
        return False

    def print_stat(self):
        """
        Debugging method for printing out available queues
        """
        print "CURRENT TDM STAT: SS/AS/AA : {}/{}/{} - ".format(
            self.speak_stack.length(),
            self.action_stack.length(),
            self.active_actions.length()
        )


def delay(time):
    now = timer()
    while timer()-now < time:
        pass


class sent_test(object):
    def __init__(self):
        self.start_time = timer()
        self.sent = []
        self.delay = []

    def add_sentece(self, sent, delay):
        self.sent.append(sent)
        self.delay.append(delay)

    def get_sent(self):
        if self.sent != []:
            if timer()-self.start_time > self.delay[0]:
                self.delay.pop(0)
                return self.sent.pop(0)
        return None



if __name__ == "__main__":
    obj = TDM()
    obj.turn_on()
    start = timer()
    sent = sent_test()
#    sent.add_sentece("Tell me a joke", 2)
#    sent.add_sentece("Who is there", 5)
#    sent.add_sentece("who", 9)
    sent.add_sentece("screen", 2)
    sent.add_sentece("press start button", 8)
#    sent.add_sentece("", 10)
    run_obj = True
    runMain = True
    window2 = True
    while True:

        say = sent.get_sent()
        if say != None:
            obj.add_to_word_bag(say)

        obj.silent_run()

        delay(.2)

        if not obj.speak_stack.isEmpty():
            temp = obj.get_speak_stack()
            if temp != None:
                print "main Speak_stack : {}".format(temp.msg)


        if not obj.action_stack.isEmpty():
            temp = obj.action_stack.pop()

        if timer()-start > 4:
            if not obj.active_actions.isEmpty():
                print "Forcing from active action stack {}, {}".format(
                    obj.active_actions.stack[0].msg,
                    obj.active_actions.stack[0].id()
                )
                if not obj.active_actions.isEmpty():
                    idval = obj.active_actions.stack[0].id()
                    obj.active_actions.add_finished_id(
                        idval
                    )
        if runMain and timer()-start > 4:
            print "Mock return value main"
            window_panel = obj.get_storage()
            window_panel.update("main")
            runMain  = False

        if window2  and timer()-start > 8:
            print "Mock return value power_up"
            window_panel = obj.get_storage()
            window_panel.update("blabla_pin")
            window2  = False


        if timer()-start > 25:
            obj.turn_off()
            while timer()-start < 26:
                None
            print "Timeout Exit"
            break
