#!/usr/bin/env python
#nameDatabase.py
"""Create a class specific structure of a database containing name and 
information of persons. The class uses a query method of checking if name
is in database, comparing to a string output and then returns the object
regarding the person.
Author :    David Orn
            david@iiim.is
(c)iiim.is"""

import json, os, logging, exceptions

#DEBUGGING REMOVE
import numpy as np

# Define a logger for object
logger = logging.getLogger(__name__)

# MAIN OBJECT CONTAINING ALL NAMES AND INFORMATION FROM DATABASE

# DISCLAIMER
# CAN'T PROCESS 2 NAMES AT A TIME, E.G. "CALL JESUS, CARLOS AND 
# RODRIGUES. CAN TAKE ONE ARUGMENT AND RETURN ALL POSSIBLE NAMES
# EG. CALL JESUS <- [<INSTANCE_NAME==JESUS_RODRIGES><INSTANCE_NAME==JESUS_MIGUEL> ETC]

class NameClass():
    """Contains a set of all names in the database
    created from nameDatabase.json located in current
    directory"""
    def __init__(self):
        self.size  = 0
        self.name_list = []
    

    def add_name(self, name_item):

        self.name_list.append([name_item.first_name.lower(), 
                               name_item.last_name.lower(),
                               name_item])
        self.size += 1
    
    def sort(self):
        self.name_list = sorted(self.name_list, key= lambda x:x[0])

    def query_first_name(self, f_name):
        it = iter(self.name_list)
        return_value = None
        first_letter = f_name[0]
        while True:
            item = next(it, None)
            if item:
                name = item[0]
                if first_letter >= name[0]:
                    if f_name == name:
                        if return_value:
                            return_value.append(item[2])
                        else :
                            return_value = [item[2]]

                else : 
                    break # Passed the alphabet value

            else :
                break
        return return_value



    def query_last_name(self, dataset, l_name):
        return_value = None
        for name_item in dataset:
            if l_name in name_item.last_name.lower() :
                if return_value:
                    return_value.append(name_item)
                else :
                    return_value = [name_item]

        return return_value

  

    def search(self, inputSentence):
        # Given a name return a json object containing all information
        # TODO Redefine how method is done, need to think about what structure
        name, probable = [], []

        ######### Search sentance word for word,
        # Ensuring words are split
        if not type(inputSentence) is tuple:
            if isinstance(inputSentence, basestring):
                inputSentence = (inputSentence.lower()).split(" ")
            else :
                # * * * * * * * * * SPECIAL NOTICE * * * * * * * * * * * * 
                # IF THIS THROWS AN ERROR THE WHOLE TDM CAN CRASH.........
                # If input is deformed (not a touple of strings) throw error
                # 
                logger.info("Sentance '{}' no a string".format(inputSentence))
                raise exceptions.TypeError()

        # Here we assume that inputSentence has been split

        name_holder = []
        full_name = []
        has_name = False
        # Create an iterator over the sentance
        it = iter(inputSentence)
        while True:
            # Get next word in sentence
            new_word = next(it, None)

            if new_word and not has_name: # Not empty and not found a name
                # If name is in the dictionary, return set of possible 
                # values
                name_holder = self.query_first_name(new_word)
                # Let the rest of the program know we have a first name
                if  name_holder:
                    has_name = True
            # Enters here if on the previous word it found a first name
            elif new_word and has_name: # Not empty and previously found first name
                # Query the dictionary to see if there are many last names
                # reurn, test value : name found True/False and 
                # values Either a set of names or one name
                full_names = self.query_last_name(name_holder, new_word)
                # Assuming a last name was found, either a set of values
                # or one value is returned
                if full_names:
                    # Unpack values into a return touple, a certain name value
                    for value in full_names:
                        if name:
                            name.append(value)
                        else :
                            name = [value]
                # If the last name test failed we can append the previous dict
                # value, name holder, and return it in a probable 
                else: 
                    for val in name_holder:
                        if probable:
                            probable.append(val)
                        else :
                            probable = [val]
                # Clean variables 
                name_holder = []
                has_name = False
            # No new word == end of iter, if we still hold a name return 
            # probable name, otherwise return previously set None, break 
            # to stop the while loop
            else : 
                if has_name:
                    for val in name_holder:
                        if probable:
                            probable.append(val)
                        else :
                            probable = [val]
                break

        #########    
        return name, probable






# ITEMS OF NAM CREATED FROM READING DATABASE FILE
class NameItem():
    def __init__(self, first_name, last_name, hometown, phone_number, email):
        self.first_name     = first_name
        self.last_name      = last_name
        self.hometown       = hometown
        self.phone_number   = phone_number
        self.email          = email


    @staticmethod
    def decoder(obj):
        name = obj["name"]
        f_name = name["first"]
        l_name = name["last"]

        return NameItem(f_name, l_name, obj["hometown"],
                      obj["phoneNumber"], obj["email"])

# FUNCTIONS TO CREATE THE DATABASE
def load_database():
    db = NameClass()
    with open(load_database_file(), 'rU') as fptr:
        for line in fptr:
            json_obj = json.loads(line)
            nameObj = NameItem.decoder(json_obj)
            db.add_name(nameObj)

    db.sort()

    return db

def load_database_file():
    db_name = "nameDatabase.json"
    fid     = None
    for root, dirs, files in os.walk('../'): 
        # Unix method, check all structure one 
        # level above current level
        for name in files:
            if db_name in name and "json" == name[-4:]:
                fid = os.path.join(root, name)

    return fid


if __name__ == "__main__":
    db = load_database()
    print db.size
    val = np.zeros(db.size)
    count = 0
    

    testSentence = "this is a test testing dillon domiano and henry linker also we want to test james the third henry sitton and others maby louis holiday and other louis"
    print testSentence
    names, prob = db.search(testSentence)
    for name in prob:
        print "Possibly {} {}".format(name.first_name, name.last_name)
    for name in names:
        print "Sure {} {}".format(name.first_name, name.last_name)



#    for k in db.name_item:
#        t1 = k.last_name
#        for l in db.name_item:
#            t2 = l.last_name
#            if t1 in t2:
#                val[count] += 1 
#
#        count += 1
#
#    for n in range(db.size):
#        print "{} : {} \n".format(db.name_item[n].last_name, val[n])
#

