#!/usr/bin/env python
#nameDatabase.py
"""Create a class specific structure of a database containing name and 
information of persons. The class uses a query method of checking if name
is in database, comparing to a string output and then returns the object
regarding the person.
Author :    David Orn
            david@iiim.is
(c)iiim.is"""

import json, os

# MAIN OBJECT CONTAINING ALL NAMES AND INFORMATION FROM DATABASE
class NameClass():
    """Contains a set of all names in the database
    created from nameDatabase.json located in current
    directory"""
    def __init__(self):
        self.nameItem = []
        self.size  = 0
        self.list_of_first_names = []
        self.list_of_last_names  = []
        self.list_of_names = []

    def add_name(self, name):
        self.nameItem.append(name)
        self.list_of_first_names.append(name.first_name)
        self.list_of_last_names.append(name.last_name)

        name = name.first_name + " " + name.last_name
        self.list_of_names.append(name)
        self.size += 1

    def search(self, inputSentence):
        # Given a name return a json object containing all information
        # TODO Redefine how method is done, need to think about what structure
        # is best
        pass




# ITEMS OF NAME CREATED FROM READING DATABASE FILE
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
    print(db.size)


