from datetime import datetime

def getNumNullops(duration, max_sample=1.0):
    """Return number of do-nothing loop iterations."""
    for amount in [2**x for x in range(100)]:  # 1,2,4,8,...
        begin = datetime.now()
        for ii in xrange(amount): pass
        elapsed = (datetime.now() - begin).total_seconds()
        if elapsed > max_sample:
            break
    return int(amount/elapsed*duration)

if __name__ == '__main__':
    print(getNumNullops(1.0))
