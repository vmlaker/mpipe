from mpipe import Stage, OrderedWorker, FilterStage, Pipeline

class Echo(OrderedWorker):
    def doTask(self, value):
        print(value)

s1 = Stage(Echo, do_stop_task=True)
p1 = Pipeline(s1)

s2 = FilterStage(
    (p1,),
    max_tasks=999,
    do_stop_task=True,
    )
p2 = Pipeline(s2)

for number in range(10):
    p2.put(number)

p2.put(None)
