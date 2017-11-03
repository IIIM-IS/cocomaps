#!/usr/bin/env python2.7
#/home/david/IIIM/Projects/cocomaps/MEx/smallCalcs.py
import os, shutil
import numpy as np


# Here are some helping functins regarding making the MEx file structure
# and some minor calcs or admin functions.

def createTemplateStructure():
    # Copy the names of the tasks in the TDM folder and
    # create template structures based on names. E.g.
    # given AskForInput we have a template with subtasks
    # available
    files = []
    for _, _, fileList in os.walk("/home/david/IIIM/Projects/cocomaps/tdm2/Modules/tasks"):
        for file in fileList:
            files.append(file)

    for file in files:
        fid = 'templates/'+file
        with open(fid, 'w') as fout:
            fout.write("""{"__type__":"template",\n""")
            fout.write("""\t "name": """+file+",\n" )
            fout.write("""\t "query": []\n """)
            fout.write("}\n")

def createTaskBackup():
    # Create a backup of the tasks files 
    dirName = "/home/david/IIIM/Projects/cocomaps/tdm2/Modules/tasks"
    dirBak = "/home/david/IIIM/Projects/cocomaps/tdm2/Modules/tasks_bak"

    if os.path.isdir(dirBak):
        shutil.rmtree(dirBak)
    shutil.copytree(dirName, dirBak)

def addLineToList():
    # Copy the entire tdm2/Modules/task folder to tasks_bak
    # create a new empty folder of task and add the following 
    # to structure

    createTaskBackup()

    dirName = "/home/david/IIIM/Projects/cocomaps/tdm2/Modules/tasks"
    dirBak = "/home/david/IIIM/Projects/cocomaps/tdm2/Modules/tasks_bak"
    for fileName in os.listdir(dirBak):
        tempFile = dirBak+"/"+fileName
        newFile = dirName+"/"+fileName
        text = []
        with open(newFile, 'w') as fin:
            with open(tempFile, 'r') as fout:
                for line in fout:
                    if "isActive" in line:
                        fin.write('    "isActive": "False", \n')
                        fin.write('    "query": []\n')
                    else :
                        fin.write(line)

def printContentOfTasks():
    # Having some issue with the tasks, need to print out the values to ensure
    # they are all there
    dirName = "/home/david/IIIM/Projects/cocomaps/tdm2/Modules/tasks/"
    for fileName  in os.listdir(dirName):
        print(fileName)
        with open(dirName+fileName, 'r') as fptr:
            temp = fptr.read()
            print(temp)

def testIsStringMethod():
    a = "This is a string"
    b = lambda x: x**2

    print(isinstance(a, basestring))
    print(isinstance(b, basestring))

def numpyTesterAccess():
    arr = np.random.randn(10)
    loc = [1,3,4]
    print(arr)
    print(arr[loc])


if __name__ == "__main__":
    numpyTesterAccess()
    print("Finished running smallCalcs.py")
