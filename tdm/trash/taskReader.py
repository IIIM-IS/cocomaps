# Debug function for tasks

import os

loc = "Modules/tasks/"

def fixBracket(loc):
    for filename in os.listdir(loc):
        fid = loc + filename
        with open(fid, 'r') as file:
            text = ""
            for line in file:
                if "functionCalls" in line:
                    cutStr = line.split(':')
                    values = cutStr[1][:-3]
                    outStr = "[]"
                    if not "" == values:
                        outStr = cutStr[0]+ ' : [' + values + '],\n'
                    text = text + outStr
                else :
                    text = text + line
        with open(fid, 'w') as file:
            file.write(text)

def removeEmptyString(loc):
    for filename in os.listdir(loc):
        fid = loc + filename
        with open(fid, 'r') as file:
            text = ""
            for line in file:
                if "functionCalls" in line:
                    cutStr = line.split(':')
                    values = cutStr[1][:-3]
                    if '""' in values :
                        outStr = '    "functionCalls" : [], \n'
                        text = text+outStr
                    else: 
                        text = text+line
                else :
                    text = text + line
            print(text)
        with open(fid, 'w') as file:
            file.write(text)

def general():
    for filename in os.listdir(loc): 
        fid = loc + filename
        with open(fid, 'r') as file:
            # for line in file:
            #    if "prerequisites" in line:
    # Read task in taskList
            start = 0 
            for line in file:
                if "taskList" in line:
                    start = 1
                if start == 1:
                    print(line)
                if "]" in line:
                    start = 0
                       

def generalPrintLine(loc):
    for filename in os.listdir(loc): 
        fid = loc + filename
        with open(fid, 'r') as file:
            for line in file:
                if "functionCall" in line:
                    print(line)

removeEmptyString(loc)
