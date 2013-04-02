import sys
import mpipe

def forloop(amount):
    for ii in xrange(amount): pass

stage = mpipe.UnorderedStage(forloop, 2)
pipe = mpipe.Pipeline(stage)

for foobar in range(5): 
    pipe.put(int(sys.argv[1]))

pipe.put(None)
