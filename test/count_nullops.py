from datetime import datetime
from builtins import range


def get_num_null_ops(duration, max_sample=1.0):
    """Return number of do-nothing loop iterations."""
    for amount in [2**x for x in range(100)]:  # 1,2,4,8,...
        begin = datetime.now()
        for ii in range(amount):
            pass
        elapsed = (datetime.now() - begin).total_seconds()
        if elapsed > max_sample:
            break
    return int(amount/elapsed*duration)


if __name__ == '__main__':
    print(get_num_null_ops(1.0))
