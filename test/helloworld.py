import mpipe


def echo(value):
    print(value)


def main():
    stage = mpipe.OrderedStage(echo)
    pipe = mpipe.Pipeline(stage)

    for val in (0, 1, 2, 3):
        pipe.put(val)

    pipe.put(None)  # Stop the pipeline.


if __name__ == '__main__':
    main()
