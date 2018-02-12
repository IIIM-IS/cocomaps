
# Objective : See if a dictionary call to function can return two values



def funA(*args):
    if args:
        _dict = args[0]
    else:
        _dict = {"Name":"FunA"}
    return False, _dict

def funB():
    return funA({"Name":"FunB"})

a = {1:funA, 2:funB}


f1 = a[1]
f2 = a[2]


res1a, res1b = f1()
res2a, res2b = f2()


print res1a, res1b["Name"],
print res2a, res2b["Name"]
