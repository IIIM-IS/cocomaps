
import json
import Tasks_def

temp_decoder = Tasks_def._Type.obj_decoder

with open("Tasks/start_generator.json", 'rb') as fid:
    txt = json.loads(fid.read())
    obj = temp_decoder(txt)

if "up" in obj.dictionary.keys():
    print "Up is in dict"
print obj.dictionary.keys()

