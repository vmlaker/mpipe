"""Implements OrderedStage class."""

from .Stage import Stage
from .OrderedWorker import OrderedWorker

class OrderedStage(Stage):
    """A specialized :class:`~mpipe.Stage`, 
    internally creating :class:`~mpipe.OrderedWorker` objects."""
    def __init__(self, target, size=1, disable_result=False):
        """Constructor takes a function implementing 
        :meth:`OrderedWorker.doTask`."""
        class wclass(OrderedWorker):
            def doTask(self, task):
                return target(task)
        super(OrderedStage, self).__init__(wclass, size, disable_result)
