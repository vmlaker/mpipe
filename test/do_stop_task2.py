from mpipe import Stage, OrderedWorker, FilterStage, Pipeline

class Echo(OrderedWorker):
    def doTask(self, value):
        print(value)

s1 = Stage(Echo, do_stop_task=True)
s2 = FilterStage(
    (s1,), 
    max_tasks=999,
    do_stop_task=True,
    )
pipe = Pipeline(s2)
for number in range(10):
    pipe.put(number)

pipe.put(None)
