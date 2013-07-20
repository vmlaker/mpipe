from mpipe import OrderedStage, Pipeline

def yes(value):
    return value

pipe = Pipeline(OrderedStage(yes, disable_result=True))

for number in range(10):
    pipe.put(number)

pipe.put(None)

for result in pipe.results():
    print(result)
