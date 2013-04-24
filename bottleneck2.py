import time
from mpipe import OrderedStage, Pipeline

def echo(value):
    print(value)
    time.sleep(0.125)
    return value

pipe1 = Pipeline(OrderedStage(echo, 2))
for number in range(10):
    pipe1.put(number)
    time.sleep(0.100)

pipe1.put(None)
