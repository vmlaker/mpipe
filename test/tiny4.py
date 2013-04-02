import mpipe

class Incrementor(mpipe.UnorderedWorker):
    def doTask(self, value):
        result = value + 1
        self.putResult(result)

class Doubler(mpipe.UnorderedWorker):
    def doTask(self, value):
        result = value * 2
        self.putResult(result)

stage1 = mpipe.Stage(Incrementor, 3)
stage2 = mpipe.Stage(Doubler, 3)
stage1.link(stage2)
pipe = mpipe.Pipeline(stage1)

for number in range(10):
    pipe.put(number)
pipe.put(None)

for result in pipe.results():
    print(result)
