from mpipe import OrderedStage, Pipeline

def increment(value):
    return value + 1

def double(value):
    return value * 2

def echo(value):
    print(value)

stage1 = OrderedStage(increment)
stage2 = OrderedStage(double)
stage3 = OrderedStage(echo)
stage1.link(stage2)
stage2.link(stage3)
pipe = Pipeline(stage1)

for number in range(10):
    pipe.put(number)

pipe.put(None)
