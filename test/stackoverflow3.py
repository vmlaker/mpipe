# Solution for http://stackoverflow.com/questions/8277715
# 
# Uses UnorderedWorker objects and overcomes the problem 
# expressed in Idea 2 by running a "getter" process that
# pulls the same number of output results as the input
# count, before pushing the "stop" task on thie pipeline.

import multiprocessing
import mpipe

class Doubler(mpipe.UnorderedWorker):
    def doTask(self, value):
        return value * 2
class Printer(mpipe.UnorderedWorker):
    def doTask(self, value):
        # This is the last stage. Since we don't want any values
        # potentially lost, we set the pipeline result here,
        # thus requiring the client to call get().
        print(value)
        return True

s1 = mpipe.Stage(Doubler, 2)
s2 = mpipe.Stage(Printer, 1)
s1.link(s2)
p = mpipe.Pipeline(s1, (s2,))

def getter():
    for ii in range(1,60000):
        p.get()
g = multiprocessing.Process(target=getter)
g.start()

for ii in range(1,60000):
    p.put(ii)

g.join()
p.put(None)

# The end.
