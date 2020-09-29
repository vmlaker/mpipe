# import sys
from builtins import range
from mpipe import (UnorderedStage, Pipeline)


def increment(value):
    return value + 1


class Pull:
    def __init__(self, pipe):
        self.pipe = pipe

    def __call__(self, value):
        for result in self.pipe.results():
            print(result)


def main():
    pipe = Pipeline(UnorderedStage(increment))
    pipe2 = Pipeline(UnorderedStage(Pull(pipe)))
    pipe2.put(True)

    # for task in range(sys.maxint):
    for task in range(10000):
        pipe.put(task)
    pipe.put(None)

    pipe2.put(None)


if __name__ == '__main__':
    main()
