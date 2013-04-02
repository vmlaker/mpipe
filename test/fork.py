from mpipe import OrderedWorker, Stage, Pipeline

class Incrementor(OrderedWorker):
    def doTask(self, value):
        return value + 1

class Doubler(OrderedWorker):
    def doTask(self, value):
        return value * 2

class Printer(OrderedWorker):
    def doTask(self, value):
        print(value)

stage1 = Stage(Incrementor)
stage2 = Stage(Doubler)
stage3 = Stage(Printer)
stage4 = Stage(Printer)

stage1.link(stage2)
stage1.link(stage3)
stage2.link(stage4)

pipe = Pipeline(stage1)

for number in range(10):
    pipe.put(number)

pipe.put(None)
