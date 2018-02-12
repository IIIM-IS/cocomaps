import copy

class temper(object):
    def __init__(self):
        self.value = 0
        self.previous = None
        self.name = "Names"

mex = {}
mex["1"] = temper()


obj1 = mex["1"]
obj2 = copy.deepcopy(mex["1"])

obj1.value = 2

print("{} : {}".format(obj1.value, obj2.value))
    
