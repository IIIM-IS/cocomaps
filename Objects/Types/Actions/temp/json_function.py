import json


def print_func_name(obj):
    print obj.name


func = {"print_func_name":print_func_name}

class EncodeFunction(object):
    def __init__(self, name, descriptin, func_name):
        self.name = name
        self.description = descriptin
        self.func = func[func_name]

    @staticmethod
    def obj_decoder(obj):
        return EncodeFunction(obj["name"], obj["description"], obj["func"])

with open("func_test.json", 'rb') as fid:
    text = fid.read()
    obj = json.loads(text, object_hook=EncodeFunction.obj_decoder)


obj.func()

