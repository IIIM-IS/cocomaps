#!/usr/bin/env python2.7
# makeDatabase.py
"""
    Take the file wordMatrix.csv and create a database compilation
    to reduce probabilty of wrong inputs.

    Author
                David Orn - david@iiim.is
    Copyright 
                (c)IIIM - http://iiim.is
"""

import csv
import numpy as np


class NotEqualToZero(Exception):
    # A file specific error
    pass

def makeDatabase():
    word = {}   
    valueNames = []
    n = []

    # This file needs to be called from the MEx file
    # loaction
    with open("databases/wordMatrix.csv", 'r') as csvReader:
        fileRead = csv.reader(csvReader, delimiter=',')
        rowCount = 0
        for row in fileRead:
            if rowCount == 0:
                valueNames=row[1:]
                rowCount += 1
            else :
                word[row[0]] = [float(i) for i in row[1:]]
                if not n:
                    n = float(len(row[1:]))


    for key in word.keys():
        arrSum = np.sum(word[key])
        # Ensure that each probabilistic value sums to 1
        if not arrSum == 1:
            raise NotEqualToZero("Name value not equal to zero in wordMatrix.cls : %s" %str(key))
    print("Created new word value matrix from wordMatrix.csv")

    np.save("databases/wordMatrix.npy", [valueNames, word])    

