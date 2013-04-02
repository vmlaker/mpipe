import sys
from mpipe import UnorderedStage, Pipeline

def increment(value):
    return value + 1

stage = UnorderedStage(increment)
pipe = Pipeline(stage)

def pull(value):
    for result in pipe.results():
        print(result)

pipe2 = Pipeline(UnorderedStage(pull))
pipe2.put(True)

for task in xrange(sys.maxint):
    pipe.put(task)

pipe.put(None)
pipe2.put(None)
