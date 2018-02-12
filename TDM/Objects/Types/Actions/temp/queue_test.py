from Queue import Queue


q = Queue()
for i in range(10):
    q.put(i)
    print i

print q.qsize()

while q.qsize() != 0:
    print q.get()
