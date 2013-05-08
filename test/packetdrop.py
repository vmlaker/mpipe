from mpipe import OrderedStage, FilterStage, Pipeline
import time

def echo(value):
    print(value)
    time.sleep(0.0125)
    return value

pipe1 = Pipeline(
    FilterStage(
        (OrderedStage(echo),),
        max_tasks=2
        )
    )

def pull(task):
    for result in pipe1.results(): pass
pipe2 = Pipeline(OrderedStage(pull))
pipe2.put(True)
pipe2.put(None)

for number in range(10):
    pipe1.put(number)
    time.sleep(0.0100)

pipe1.put(None)
