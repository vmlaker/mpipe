"""Solution for http://stackoverflow.com/questions/8277715"""

from mpipe import OrderedStage, Pipeline

def f2(value):
    return value * 2

def f3(value):
    print(value)

s1 = OrderedStage(f2, size=2)
s2 = OrderedStage(f3)
s1.link(s2)
p = Pipeline(s1)

def f1():
    for task in [1,2,3,4,5,None]:
        p.put(task)

f1()
