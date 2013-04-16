import mpipe
import time

def echo(value):
    time.sleep(0.125)
    print(value)
    return True

pipe2 = mpipe.Pipeline(mpipe.OrderedStage(echo))

class Filter(mpipe.OrderedWorker):

    def __init__(self):
        self.count = 0

    def doTask(self, value):
        if self.count == 0:
            pipe2.put(value)
            self.count += 1

        elif self.count == 1:
            valid, result = pipe2.get(0.00001)
            if valid:
                self.putResult(result)
                self.count -= 1
            pipe2.put(value)
            self.count += 1

        elif self.count == 2:
            valid, result = pipe2.get(0.00001)
            if valid:
                self.putResult(result)
                pipe2.put(value)
                valid, result = pipe2.get(0.00001)
                if valid:
                    self.putResult(result)
                    self.count -= 1

pipe1 = mpipe.Pipeline(mpipe.Stage(Filter))

for number in range(10000):
    time.sleep(0.001)
    pipe1.put(number)

pipe1.put(None)
pipe2.put(None)

for result in pipe1.results():
    pass
