from mpipe import OrderedStage, FilterStage, Pipeline
import time

def echo(value):
    print(value)
    time.sleep(0.0125)
    return value

pipe1 = Pipeline(OrderedStage(echo))
pipe2 = Pipeline(FilterStage(pipe1))

def pull(task):
    for result in pipe2.results():
        pass
pipe3 = Pipeline(OrderedStage(pull))
pipe3.put(True)

for number in range(10):
    pipe2.put(number)
    time.sleep(0.0100)

pipe1.put(None)
pipe2.put(None)
pipe3.put(None)
