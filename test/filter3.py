import time
from mpipe import (OrderedStage, FilterStage, Pipeline)


def pass_thru(value):
    time.sleep(0.013)
    return value


class Pull:
    def __init__(self, pipe):
        self.pipe = pipe

    def __call__(self, task):
        for result in self.pipe.results():
            if result:
                print(result)


def main():
    s1 = FilterStage(
        (OrderedStage(pass_thru),),
        max_tasks=1,
        drop_results=True,
        )
    p1 = Pipeline(s1)

    p2 = Pipeline(OrderedStage(Pull(p1)))
    p2.put(True)

    for number in range(10):
        p1.put(number)
        time.sleep(0.010)

    p1.put(None)
    p2.put(None)


if __name__ == '__main__':
    main()
