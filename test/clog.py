# import sys
from builtins import range
from mpipe import (UnorderedStage, Pipeline)


def increment(value):
    return value + 1


def main():
    stage = UnorderedStage(increment)
    pipe = Pipeline(stage)

    # for task in range(sys.maxint if sys.version_info.major <= 2 else sys.maxsize):
    for task in range(10000):
        pipe.put(task)

    pipe.put(None)

    for result in pipe.results():
        print(result)


if __name__ == '__main__':
    main()
