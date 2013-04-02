import sys
from mpipe import UnorderedStage, Pipeline

def increment(value):
    return value + 1

stage = UnorderedStage(increment)
pipe = Pipeline(stage)

for task in xrange(sys.maxint):
    pipe.put(task)

pipe.put(None)

for result in pipe.results():
    print(result)
