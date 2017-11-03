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
debugging = True
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
db      = np.load("databases/wordMatrix.npy")
wordMatrixHeader       = db[0]
word    = db[1]


# * * * * * * * * * * *DEFINITION OF TASK RESULTS * * * * * * * * * 
def task(inputText):
    outputName = ["MakeACall", "ScheduleMeeting", "AnswerQuestion"]
    columnNumber = getColumnNumberFromName(outputName)
    print(inputText)
    print(columnNumber)
    prob = np.zeros(len(outputName))
    for word in inputText:
        temp = raceHolder(columnNumber, word)
        prob = prob + temp
        print(prob)



def who(inputText):
    # Here we search the name database from a csv file.
    print("We will try to search for a name")
    #TODO impliment name searching function
    # This obviously has increadible complexity
    # regarding input variance (i.e. the input
    # name will mist likely never be 100 accurate)


# * * * * * * * * * * *DEFINITION OF TASK RESULTS * * * * * * * * * 

def raceHolder(columnNumber, inputWord):
    # based on an input word tries to lookup in text
    n = len(columnNumber)
    out = np.zeros(n)
    try :
        percentage = word[inputWord]
        print(percentage)
        logger.debug("inputWord exists %s" %inputWord)
        out = percentage[columnNumber]
        print("Finished the try with:")
        print(out)

    except :
        logger.debug("Word NOT exists: %s" %inputWord)

    return out


def getColumnNumberFromName(names):
    # Get the header number by comparing the array of
    # headers for the wordMatrix.cls file with each 
    # word
    # I.e. get the numerical value of the column that
    # will be queried
    out = []
    for name in names:
        out.append(wordMatrixHeader.index(name))
    return out


dbDict = {"task" : task, 
          "who"  : who}

def timer():
    return int(round(time.time()*1000))

# Class definition of the meaning extractor (MEx)
class MEx():
    def __init__(self, texthandle, query):
        self.debug = 1 
        self.inputText = self.ensuretext(texthandle)
        self.query = query
        self.start = timer()
        self.daemon = True
        self.timout = 10 # Perhaps we don't need to timeout
        logger.info("Started new MEx instance")
        logger.info(query)
        logger.info("Input: " + texthandle)

        
        for q in query:
            dbDict[q](self.inputText)


    def ensuretext(self, handle):
        # Given a specific handle return a string of text
        if not isinstance(handle, basestring):
            # This might be applicable later on (@02.11.17) 
            # if the input value can be a function, a handle 
            # or other specific method, currently not used
            print("TempDebug")
            logger.info("Instance is not string")
            logger.info(type(handle))
            None
        else :
            # There should be some preprocessing on the string
            # to reduce variance and increase prob. of correct
            # identification, return a split string for further
            # processing
            #       need to get a sample of strings, 
            #       what possible errors are there
            #       to worry about
            handle = handle.split(" ")  # Split the string for 
                                        # further computation
        return handle
            



        
if __name__ == "__main__":

    if debugging:
        makeDatabase.makeDatabase()

    testStr = inStrings[random.randrange(len(inStrings))]
    temp = MEx(testStr, query)
