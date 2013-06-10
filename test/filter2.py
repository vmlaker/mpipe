import time
from mpipe import OrderedStage, FilterStage, Pipeline

def passthru(value):
    time.sleep(0.013)
    return value

s1 = FilterStage(
    (OrderedStage(passthru),), 
    max_tasks=1,
    cache_results=True,
    )
p1 = Pipeline(s1)

def pull(task):
    for task, result in p1.results():
        if result:
            print('{0} {1}'.format(task, result[0]))

p2 = Pipeline(OrderedStage(pull))
p2.put(True)


for number in range(10):
    p1.put(number)
    time.sleep(0.010)

p1.put(None)
p2.put(None)


