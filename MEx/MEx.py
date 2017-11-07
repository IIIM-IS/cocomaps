#!/usr/bin/env python2.7
#/home/david/IIIM/Projects/cocomaps/MEx/MEx.py
"""
    Thurdsay, 2. November 2017
    Author :    David Orn
                david@iiim.is
    Copyright : Icelandic Institute for Intelligent Machines (http://www.iiim.is)

"""
# Import libraries, in final version ensure that these dependencies are met
import time, logging
import numpy as np

# Debug library imported
debugging = False 
if debugging:
    from debug.mexTester import inStrings
    from debug.mexTester import query
    from databases import makeDatabase
    import random
# inputStrings are a set of input strings simulating the texthandle
# query is a set of query tests that can be sent with the texthandle


# Logging parameters
logging.basicConfig(format='[%(name)s]>[%(asctime)s]|: %(message)s', level=logging.DEBUG, filename='MEx.log')
logger = logging.getLogger(__name__)

# Get the reference dictionary used to evaluate input words
db      = np.load("Modules/MEx/databases/wordMatrix.npy")
wordMatrixHeader       = db[0]
word    = db[1]


# * * * * * * * * * * *DEFINITION OF TASK RESULTS * * * * * * * * * 
def task(inputText):
    outputName = ["MakeACall", "ScheduleMeeting", "AnswerQuestion"]
    columnNumbers = getColumnNumberFromName(outputName)
    prob = np.zeros(len(outputName))
    for word in inputText:
        temp = raceHolder(columnNumbers, word)
        prob = prob + temp
        if np.amax(prob) >= 1:
            continue
    # Returns the name of the most likely value that the 
    # sentance holds
    return outputName[columnNumbers[np.argmax(prob)]]


def who(inputText):
    # Here we search the name database from a csv file.
    print("We will try to search for a name")
    #TODO impliment name searching function
    # This obviously has increadible complexity
    # regarding input variance (i.e. the input
    # name will most likely never be 100 accurate)
    return "No one >:)"


# * * * * * * * * * * *DEFINITION OF TASK RESULTS * * * * * * * * * 

def raceHolder(columnNumber, inputWord):
    # based on an input word tries to lookup in text
    #try :
    out = np.zeros(len(columnNumber))
    if inputWord in word.keys():
        percentage = np.array(word[inputWord])
        logger.debug("inputWord exists %s" %inputWord)
        out = percentage[columnNumber]
    else :
        logger.debug("inputWord NOT exists %s" %inputWord)
    return out


    #except :
    #    logger.debug("Word NOT exists: %s" %inputWord)

    return out


def getColumnNumberFromName(names):
    # Get the header number by comparing the array of
    # headers for the wordMatrix.cls file with each 
    # word
    # I.e. get the numerical value of the column that
    # will be queried
    out = [None]*len(names)
    nameCount = 0
    for name in names:
        out[nameCount] = (int(wordMatrixHeader.index(name)))
        nameCount+=1
    return out


dbDict = {"task" : task, 
          "who"  : who}

def timer():
    return int(round(time.time()*1000))

# Class definition of the meaning extractor (MEx)
class MEx():
    def __init__(self, texthandle, query):
        # Requirements on input, query is one value (i.e.
        # an array with array[0] equal to database value)
        self.debug = 1 
        self.inputText = self.ensuretext(texthandle)
        self.query = query[0]
        self.daemon = True
        self.timout = 10 # Perhaps we don't need to timeout
        logger.info("Started new MEx instance")
        logger.info(query)
        logger.info("Input: " + texthandle)
        self.value =  dbDict[self.query](self.inputText)

    def ensuretext(self, handle):
        # Given a specific handle return a processed string
        # or an empty value 
        logger.debug("Running MEx.ensuretext with : " + handle)
        if not isinstance(handle, basestring):
            print("TempDebug")
            logger.info("Instance is not string")
            None
        else :
            # Split the string for further computation
            handle = handle.split(" ")  
                                        
        return handle
            


        
if __name__ == "__main__":

    if debugging:
        makeDatabase.makeDatabase()

    testStr = inStrings[random.randrange(len(inStrings))]
    temp = MEx(testStr, query)
