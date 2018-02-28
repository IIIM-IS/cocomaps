
val1 = ["one"]
val2 = ["two","three","four"]
val3 = ["four", "five", "six"]

all = []
all.append(val1)
all.append(val2)
all.append(val3)


all_new = [item for line in all for item in line]

print all_new
