from mpipe import (Stage, OrderedWorker, Pipeline)


class Echo(OrderedWorker):
    def doTask(self, value):
        print(value)


def main():
    stage = Stage(Echo, do_stop_task=True)
    pipe = Pipeline(stage)

    for number in range(10):
        pipe.put(number)
    pipe.put(None)


if __name__ == '__main__':
    main()
