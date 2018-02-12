

list_a = ['morocco', 'Swinehound']
for idx, item in enumerate(list_a):
    print "{} : {}".format(idx,item)

list_a = None
if list_a:
    for idx, item in enumerate(list_a):
        print "{} : {}".format(idx, item)
