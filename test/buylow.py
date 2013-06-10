from collections import deque
import numpy as np
from mpipe import OrderedWorker, Stage, OrderedStage, Pipeline

last10 = deque()
junk = 'http://ws.cdyne.com/delayedstockquote/delayedstockquote.asmx/GetQuote?StockSymbol=fac&LicenseKey=0'
j = 'http://www.google.com/ig/api?stock=AAPL'

class Accumulator(OrderedWorker):
    def doTask(self, price):
        if last10:
            if price < min(last10):
                self.putResult(price)
        last10.append(price)
        if len(last10) > 10:
            last10.popleft()

def echo(value):
    print('value = {0}'.format(value))

stage1 = Stage(Accumulator)
stage2 = OrderedStage(echo, 50)
stage1.link(stage2)
pipe = Pipeline(stage1)

SIZE = 1000
prices = np.linspace(0, np.pi*10, SIZE)
prices = np.sin(prices) + 1
for price in prices:
    pipe.put(price)

pipe.put(None)
