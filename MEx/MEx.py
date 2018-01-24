#!/usr/bin/env python2.7
#/home/david/IIIM/Projects/cocomaps/MEx/MEx.py
"""
    Thurdsay, 2. November 2017
    Author :    David Orn
                david@iiim.is
    Copyright : Icelandic Institute for Intelligent Machines (http://www.iiim.is)

"""
# Import libraries, in final version ensure that these dependencies are met
import time, logging, os
import numpy as np

# Debug library imported
debugging = False
if debugging:
    from debug.mexTester import inStrings
    from debug.mexTester import query
    import database.buildDatabase as buildDatabase
    import random
    from database.nameDatabase import load_database

# inputStrings are a set of input strings simulating the texthandle
# query is a set of query tests that can be sent with the texthandle
else : 
    #Load a new instance of the database
    dbFolder = __file__[:-7]+"databases/"
    os.sys.path.insert(0,dbFolder)
    import database.buildDatabase as buildDatabase
    from database.nameDatabase import load_database

# Build word database from file
global DB
DB = buildDatabase.makeDataBase()

# Logging parameters
logging.basicConfig(format='[%(name)s]>[%(asctime)s]|: %(message)s', 
                    level=logging.DEBUG, 
                    filename='MEx.log')
logger = logging.getLogger(__name__)



class MEx():
    def __init__(self):
        logger.info("Starting up MEx")
        self.text = ""
        self.template = ""
        self.name_db = load_database()
        self.daemon = True

    def computeWords(self, text):
        logger.info("Checking sentance: {}".format(text))
        words = self.ensuretext(text)
        evalued = self.checkDictionary(words)

        returnItem = [None]*DB.associatesCount
        for i in range(DB.associatesCount):
            returnItem[i] = DB.associates[i], evalued[i]
            
        return sorted(returnItem, key=lambda x: x[1], reverse=True)    


    def ensuretext(self, handle):
        # Given a specific handle return a processed string
        # or an empty value 
        logger.debug("Running MEx.ensuretext with : " + handle)
        if not isinstance(handle, basestring):
            logger.info("Instance is not string")
            logger.info(type(handle))
            return None
        else :
            # Split the string for further computation
            handle = handle.lower()
            handle = handle.split(" ")  
                                        
        return handle
  
    def search_name(self, handle):
        return self.name_db.search(handle)



    def checkDictionary(self, words):
        # Takes in a new sentance and returns
        # the weighted probability of all possible
        # templates
        output = np.zeros(DB.associatesCount)
        for word in words: 
            associations, values = DB.get(word)
            if not values is None:
                padding_with_zeros = self.queryDB(associations, values)
                output += padding_with_zeros 
                # Used to have a short circuit, but to match multiple
                # we want to process entire sentance
        return output

    def queryDB(self, associations, values):
        temp = np.zeros(DB.associatesCount)
        counter = 0
        for value in values:
            place = DB.associates.index(associations[counter])
            temp[place] = value
            counter += 1
        return temp
            

def returnHighest(output):
    highest = np.amax(output)
    indx = np.where(output==highest)
    indx = indx[0][0]   # where returns tuple and this method short circuits
                        # if there are two values equal
    return DB.associates[indx], highest

# Deprecated
#def checkComparison(vector):
#    if np.amax(vector) >= 1:
#        return True
#    return False

        
if __name__ == "__main__":
    # Prints out the entire database
    MExObject = MEx()
    teststr = ["Dear robot I would like to shedule a meeting with Shawnta Koles", "Robot call phil",
               "please ask lacy about tobi pharris"]
    for test in teststr:
        obj = MExObject.computeWords(test)
        print test
        name, poss_name = MExObject.search_name(test)
        print obj
        for thing in name:
            print "Certain : {} {}".format(thing.first_name, thing.last_name)
        for thing in poss_name:
            print "Possible : {} {}".format(thing.first_name, thing.last_name)
        print  20*'-'
        print '\n'



