#!/usr/bin/env python
#buildDatabase.py
"""
Builds the database for MEx based on accosiation file wordAccociation.txt which
should be in the same directory

Author : David Orn
         david@iiim.is
(c)IIIM.is

"""
import os 
import numpy as np

# WordNodes are in a dictionary, referenced by name, word maps to WordNode, given a
# query for a specific word, the WordNode returns two vectors, V1 contains the values
# for each represented task by that word, the second vector (V2) gives the names of the
# tasks associated with V1

class WordNode():
    """
    __init__(self, word, associationvalue, associate)
    """
    def __init__(self, word, associationvalue, associate):
        self.word = word
        self.associates = {associate : associationvalue}
        self.numberofassociations = 1

    def add_associate(self, associate, associationvalue):
        """Add association between words and concepts"""
        if associate not in self.associates.keys():
            self.associates[associate] = associationvalue
            self.numberofassociations += 1

        elif  associate in self.associates.keys() and not associationvalue == 0:
            self.associates[associate] = associationvalue


    def get(self):
        """Return associated values and relative weights """
        values = np.asarray(self.associates.values())
        names = self.associates.keys()

        return names, values

class WordDB(object):
    """Node object, contains words and associations with concepts
        using dictionary strucure"""
    def __init__(self):
        self.words = []
        self.wordnodes = {}
        self.wordcount = 0
        self.associates = []
        self.associatesCount = 0
    
    def addnode(self, word, associationvalue, association):
        if association not in self.associates:
            self.associates.append(association)
            self.associatesCount += 1
# Commented out because using this method creates a sparse matrix
# when the output is returned the values aren't always in order. 
# To fix this each word has associatons and values to those
# associations
            # Add association to words already in database
#            if not self.wordnodes:
#            # For the first pass self.wordnodes is empty
#                None
#            else :
#            # If not empty add associate to all nodes
#                for keys, nodes in self.wordnodes.iteritems():
#                    nodes.add_associate(association, 0)
        # Empty self.word first iter no availible
        if not word in self.words:
            self.words.append(word)
            NewWord = WordNode(word, associationvalue, association)
#            for associations in self.associates:
#                NewWord.add_associate(associations, 0)
            self.wordnodes[word] = NewWord
            self.wordcount += 1
        # 
        elif word in self.words:
            oldWord = self.wordnodes[word]
            oldWord.add_associate(association, associationvalue)

                
    def addWord(self, word, associate, associateValue):
        if not self.words:
            self.words.append(word)
    
    def get(self, word):
        if word in self.wordnodes:
            return self.wordnodes[word].get()
        return None, None



# FUNCTIONS FOR READING IN THE FILE AND HANDLING THE STREAM
def getDatabaseFile():
    """
        Gets the databse word association file from the current directory
    """
    db_name = "wordAssociation.txt"
    fid = ''
    curr = os.getcwd()
    for root, dirs, files in os.walk("../"):
        for name in files:
            if db_name in name and ".txt" == name[-4:]:
                fid = os.path.join(root, name)
    print "File location {}".format(fid)

    return fid

def isHeader(inline):
    # Check if line is header
    if inline[-2] == "{":
        return True
    return False

def headerRip(inline):
    # Rip the header name from the string and return string without header
    # mark
    return inline[:-2]

def makeDataBase():
    fid = getDatabaseFile()
    DB = WordDB()

    print 2*'\n'
    print 10*'*'+ "COMPILING DICTIONARY" + 10*'*'
    with open(fid, 'r') as fptr:
        inItem = False
        currHeader=""
        for line in fptr:
            if not line[0]=='*' and not line=="\n":
                if line[0]=="}":
                    inItem=False
                if isHeader(line):
                    currHeader=headerRip(line)
                    inItem = True
                else :
                    if inItem:
                        word, value = line.split('#')
                        value=float(value)
                        print "{} -  {}  -  {}".format(word, value, currHeader)
                        DB.addnode(word, value, currHeader)
    
    print 10*'*'+ "FINISHED COMPILING DICTIONARY" + 10*'*'
    print(2*'\n')
    return DB

if __name__=="__main__":
    db = makeDataBase()
    print "Word count {} associates {}".format(db.wordcount, db.associatesCount)
    
    testvals = ["meet","meeting",  "make", "horse", "ring", "ruderbagle", "schedule"]  
    print db.associates
    for t in testvals:
        val, names = db.get(t)
        print "{} -  {} - {}".format(t, val, names)
        val = db.get(t)
        print "{}  - {} ".format(val, type(val))
