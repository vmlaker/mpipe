# Solution for http://stackoverflow.com/questions/8277715
# 
# Uses UnorderedWorker objects with the last stage not
# producing output results, thus illustrating the problem 
# expressed in Idea 2: one of the two Doubler workers
# propagates the "stop" task to the next stage while
# the other worker is still processing a number, resulting
# in the value being lost.

import mpipe

class Doubler(mpipe.UnorderedWorker):
    def doTask(self, value):
        return value * 2
class Printer(mpipe.UnorderedWorker):
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
