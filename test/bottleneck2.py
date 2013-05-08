import time
from mpipe import OrderedStage, Pipeline

def echo(value):
    print(value)
    time.sleep(0.013)
    return value

pipe = Pipeline(OrderedStage(echo, 2))
for number in range(12):
    pipe.put(number)
    time.sleep(0.010)

pipe.put(None)
