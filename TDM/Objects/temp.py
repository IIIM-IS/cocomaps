#! /usr/bin/env python
#################################################################################
#     File Name           :     temp.py
#     Created By          :     david
#     Email               :     david@iiim.is
#     Creation Date       :     [2018-02-28 17:57]
#     Last Modified       :     [2018-02-28 18:12]
#     Description         :     Test various hypothesis 
#     Version             :     0.1
#################################################################################



words = "This is a sentence containing some words"


words = words.lower().split(" ")

W = []
for word in words:
    W.append(word)

print W
print W[0]

while 1:
    try :
        print W.pop(0)
    except:
        print "Couldn't pop"
        break

temp = "This"

if temp != None and temp != "":
    print temp

