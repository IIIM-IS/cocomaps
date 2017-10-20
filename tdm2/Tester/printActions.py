# Print the function calls from tasks, defined in tasks/*, to keep a list of 
# what functions need to be implimented.

from Modules.Task import *
import Modules.static

static.init()
initDictionaries('Modules/')

taskList = []
for task in static.tasks.values(): 
    if not task.functionCalls == "":
        taskList.append(task.functionCalls)

taskList.sort()
with open('Modules/actions/actions', 'w') as fid:
    fid.write('{ \n')
    for k in taskList:
        outStr = """"%s": "", \n """ %(k)
        fid.write(outStr)
    fid.write('}')
