import re

tests = [
    "This is a String of C256$haracters",
    "This is ASTRING, of ... manty !@$& th)))12i%ng",
    "So Is THis BAstar1234???:>"
]

regex = re.compile("[^a-zA-Z ]")

for line in tests:
    line = regex.sub('',line)
    temp = line.lower().split(" ")
    print temp
