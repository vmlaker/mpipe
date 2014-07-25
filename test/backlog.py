from sys import stdout
from threading import Thread
from time import sleep

from mpipe.Pipeline import Pipeline
from mpipe.UnorderedStage import UnorderedStage


def inc(x):
    sleep(0.1)
    stdout.write('+')
    return x+1

def dec(x):
    sleep(0.2)
    stdout.write('-')
    return x-1


stage1 = UnorderedStage(inc, 3, max_backlog=3)
stage2 = UnorderedStage(dec, 1, max_backlog=1)
stage1.link(stage2)
pipeline = Pipeline(stage1)


def print_results():
    for result in pipeline.results():
        stdout.write(str(result))

print_thread = Thread(target=print_results)
print_thread.start()


for i in range(10):
    sleep(0.01)
    pipeline.put(i)
    stdout.write('i')


pipeline.put(None)
print_thread.join()