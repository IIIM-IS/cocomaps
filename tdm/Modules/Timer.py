import time

def now():
    return int(round(time.time()*1000))

class Timer():
    def __init__(self):
        self.starttime = now()
        self.elapsed = 0
        self.stop = False

    def resetTimer(self):
        self.starttime = now()
        
    def check(self, maxTime):
        self.elapsed = (now() -self.starttime)
        if self.elapsed >= maxTime:
            self.stop = True
        return self.stop



