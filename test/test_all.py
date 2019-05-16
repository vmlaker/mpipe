def test_tiny(capsys):
    """ The very basic test, featured on the front page of the doc.
    """
    from mpipe import OrderedStage, Pipeline
    def increment(value):
        return value + 1
    def double(value):
        return value * 2
    stage1 = OrderedStage(increment, 3)
    stage2 = OrderedStage(double, 3)
    pipe = Pipeline(stage1.link(stage2))
    for number in range(10):
        pipe.put(number)
    pipe.put(None)
    for result in pipe.results():
        print(result)

    import os
    with open(os.path.join(os.path.dirname(__file__), 'tiny.gold')) as f:
        assert f.read() == capsys.readouterr().out


def test_tiny2(capsys):
    """ Variation on the basic test, using classes and unordered workers.
    """
    import mpipe
    class Incrementor(mpipe.UnorderedWorker):
        def doTask(self, value):
            return value + 1
    class Doubler(mpipe.UnorderedWorker):
        def doTask(self, value):
            return value * 2
    stage1 = mpipe.Stage(Incrementor, 3)
    stage2 = mpipe.Stage(Doubler, 3)
    stage1.link(stage2)
    pipe = mpipe.Pipeline(stage1)
    for number in range(10):
        pipe.put(number)
    pipe.put(None)
    for result in pipe.results():
        print(result)

    import os
    with open(os.path.join(os.path.dirname(__file__), 'tiny.gold')) as f:
        gold = (int(x) for x in f.readlines())
        test = (int(x) for x in capsys.readouterr().out.split())
        assert sorted(gold) == sorted(test)


def test_tiny3(capsys):
    """ Variation of the basic test.
    """
    import mpipe
    class Incrementor(mpipe.OrderedWorker):
        def doTask(self, value):
            result = value + 1
            self.putResult(result)
    class Doubler(mpipe.OrderedWorker):
        def doTask(self, value):
            result = value * 2
            self.putResult(result)
    stage1 = mpipe.Stage(Incrementor, 13)
    stage2 = mpipe.Stage(Doubler, 13)
    stage1.link(stage2)
    pipe = mpipe.Pipeline(stage1)
    for number in range(10):
        pipe.put(number)
    pipe.put(None)
    for result in pipe.results():
        print(result)

    import os
    with open(os.path.join(os.path.dirname(__file__), 'tiny.gold')) as f:
        assert f.read() == capsys.readouterr().out


def test_tiny4(capsys):
    """ Another variation of the basic test.
    """
    import mpipe
    class Incrementor(mpipe.UnorderedWorker):
        def doTask(self, value):
            result = value + 1
            self.putResult(result)
    class Doubler(mpipe.UnorderedWorker):
        def doTask(self, value):
            result = value * 2
            self.putResult(result)
    stage1 = mpipe.Stage(Incrementor, 3)
    stage2 = mpipe.Stage(Doubler, 3)
    stage1.link(stage2)
    pipe = mpipe.Pipeline(stage1)
    for number in range(10):
        pipe.put(number)
    pipe.put(None)
    for result in pipe.results():
        print(result)

    import os
    with open(os.path.join(os.path.dirname(__file__), 'tiny.gold')) as f:
        gold = (int(x) for x in f.readlines())
        test = (int(x) for x in capsys.readouterr().out.split())
        assert sorted(gold) == sorted(test)
