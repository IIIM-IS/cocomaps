#! /usr/bin/env python
#################################################################################
#     File Name           :     TDM.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-03-06 15:12]
#     Last Modified       :     [2018-03-09 10:00]
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
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting Supervisory Intermediate")
        self.last_action = 0 
        
        self.output_action = None
        self.dialog = Dialog()
        
        # Dynamic variables
        self.talk = False
        self.stop = False
        self.last_speak = 0
        self.current_task = None
        self.active_actions = TDM_AA()
        self.action_stack = TDM_AS(self.active_actions)
        self.speak_stack  = TDM_SS()
        self.word_bag = Word_Bag()
        self.id_number = 0

        self.speaking_timeout = 0

        # Static variables:
        self.max_timeout = 45
        self.Tasks = Task_object()
        self.MEx = MEx.MEx(self.Tasks)

    def get_speak_stack(self):
        """
        For the TDM_psyclonce call, if there is anything on the speak
        stack return it and pop the stack
        """
        #self.logger.debug("Checking speak stack")
        if not self.speak_stack.isEmpty() and self.speak_timeout():
            out_speak = self.speak_stack.pop()
            self.set_speek_timeout(out_speak.max_time)
            return out_speak
        return None
    def set_keywords(self, key, list):
        if self.current_task != None:
            self.current_task.keywords = {key, list}

    def id(self):
        self.id_number+=1
        return self.id_number-1


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
        if not self.action_stack.isEmpty():
            # Somehow add that action to the action list inherant 
            # in this TDM system and monitor the action
            data = self.action_stack.pop()
            self.active_actions.add(data)
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
        if self.current_task == None:
            if self.action_stack.history == []:
                self.logger.debug("Adding Greet to stack")
                self.set_active_task("Greet")
                self.action_stack.history.append("greet")
            else:
                self.logger.debug("Adding GetObjective to stack")
                self.set_active_task("GetObjective")


    def set_active_task(self, task_name):
        """
        Set the current task according to task name. Prepare the 
        action stack and check if information is available. If
        not create an speak_object and add on stack. If data is
        available put action_object on action stack
        """
        # TODO decide where we should put the waiting period for the
        # active action list. 
        new_task = self.Tasks.get(task_name)
        self.current_task = new_task


    def information_query(self):
        """
        Check if there is information in the speak buffer to decide 
        what is missing from the task, if not put question on Speach 
        Stack
        """
        task = self.current_task
        p = self.MEx.dict_search(task.keywords, self.word_bag)
        if p.sum() == 0:
            # Add question to stack
            self.speak_stack.add(task.primary_question(), self.id())
        else :
            self.logger.debug("Current task: {}".format(task.name))
            self.logger.debug("Current keywords: {}".format(task.keywords))
            self.logger.debug("Current p: {}".format(p))
            self.logger.debug("argmax {}".format(np.argmax(p)))
            self.logger.debug("Keyword: {}".format(task.keylist[np.argmax(p)]))

            task.set_keyword(task.keylist[np.argmax(p)])
            self.speak_stack.reset()
        



    def add_to_word_bag(self, sentence):
        """
        Try to add the Nunace input to the word bag.
        """
        self.word_bag.add(sentence)

    def silent_run(self):
        """
        Silent run gets checked each time, this pushes actions to action stack
        and ensures that enqueued text is ready

        Can return actions to be performed that don't require timed inputs

        from the user
        """
        # Check if the variable of dialog on can be set off and the system 
        # reset
        if not self.turn_dialog_off() :
            if self.active_actions.wait():

                # Check the active action stack if there are any actions
                # that require a wait period
                None
            elif self.active_actions.timeouts():
                # Check if anything in the active action has a timeout
                # First approach, reset system
                self.logger.info("Timeout ")
                self.clean_task_setup()
                self.active_actions.reset()
                self.action_stack.reset()
                self.speak_stack.reset()

            else: 
                if self.action_stack.isEmpty() and self.speak_stack.isEmpty():
                    # Special case for greeting
                    if self.current_task != None and self.current_task.name == "Greet":
                        self.clean_task_setup()
                self.check_task()

                # Check if there is a wait for information 
                if self.speak_stack.isEmpty() and self.current_task.keyword == None:
                        # Check the current active task for information
                        self.information_query()
                elif self.current_task.keyword != None:
                    self.current_task.eval(self)


    def turn_dialog_off(self):
        """
        Check when last input was recorded, if to long. Force dialog off
        """
        if self.last_action == 0:
            return False

        if timer() - self.last_action > self.max_timeout:
            self.action_stack.reset()
            return True
        return False


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
    start = timer()
    sent = sent_test()
#    sent.add_sentece("Tell me a joke", 2)
#    sent.add_sentece("Who is there", 5)
#    sent.add_sentece("who", 9)
    sent.add_sentece("move to the second location", 3)
    sent.add_sentece("second point", 8)
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
        #print "Speach timeout {}".format(obj.speaking_timeout)
        if not obj.action_stack.isEmpty():
            temp = obj.action_stack.pop()
            print "main Action Stack : {}".format(temp.msg)


        if timer()-start > 18:
            break

