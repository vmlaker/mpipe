import time
from mpipe import OrderedStage, FilterStage, Pipeline

def echo(value):
    print(value)
    time.sleep(0.125)
    return value

pipe1 = Pipeline(OrderedStage(echo))
pipe2 = Pipeline(FilterStage((pipe1,), max_tasks=2))
for number in range(10):
    pipe2.put(number)
    time.sleep(0.100)

pipe1.put(None)
pipe2.put(None)
