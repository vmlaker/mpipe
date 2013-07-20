from mpipe import OrderedStage, Pipeline

def yes(value):
    return value

stage = OrderedStage(yes, 4, disable_result=True)
pipe = Pipeline(stage)

for number in range(10):
    pipe.put(number)

pipe.put(None)

count = 0
for result in pipe.results():
    count += 1

print(count)
