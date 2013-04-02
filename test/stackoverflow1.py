# Solution for http://stackoverflow.com/questions/8277715

import mpipe

class Doubler(mpipe.OrderedWorker):
    def doTask(self, value):
        return value * 2
class Printer(mpipe.OrderedWorker):
    def doTask(self, value):
        # This is the last stage. Since we don't want the pipeline
        # to have results (don't want the client to call get()), 
        # let's not setResult() or return anything that is not None.
        print(value)

s1 = mpipe.Stage(Doubler, 2)
s2 = mpipe.Stage(Printer, 1)
s1.link(s2)
p = mpipe.Pipeline(s1, (s2,))

for ii in range(1,60000):
    p.put(ii)
p.put(None)

# The end.
