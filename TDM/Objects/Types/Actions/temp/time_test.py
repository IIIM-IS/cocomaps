from timeit import default_timer as timer
import time



start = timer()

for k in range(100):
    time.sleep(.0050)
    print timer() - start
