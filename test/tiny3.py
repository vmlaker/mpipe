import mpipe

class Incrementor(mpipe.OrderedWorker):
    def doTask(self, value):
        result = value + 1
        self.putResult(result)

class Doubler(mpipe.OrderedWorker):
    def doTask(self, value):
        result = value * 2
        self.putResult(result)

stage1 = mpipe.Stage(Incrementor, 13)
stage2 = mpipe.Stage(Doubler, 13)
stage1.link(stage2)
pipe = mpipe.Pipeline(stage1)

for number in range(10):
    pipe.put(number)
pipe.put(None)

for result in pipe.results():
    print(result)
