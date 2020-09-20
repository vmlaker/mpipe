import sys
import mpipe
from builtins import range


def for_loop(amount):
    for ii in range(amount):
        pass


def main():
    stage = mpipe.UnorderedStage(for_loop, 2)
    pipe = mpipe.Pipeline(stage)

    for foobar in range(5):
        pipe.put(int(sys.argv[1]) if len(sys.argv) >= 2 else 10)

    pipe.put(None)


if __name__ == '__main__':
    main()
