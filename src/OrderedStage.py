"""Implements OrderedStage class."""

from .Stage import Stage
from .OrderedWorker import OrderedWorker

__all__ = ['OrderedStage']


class _Worker(OrderedWorker):
    def __init__(self, task_fn):
        super(_Worker, self).__init__()
        self.task_fn = task_fn

    def doTask(self, task):
        return self.task_fn(task)


class OrderedStage(Stage):
    """A specialized :class:`~mpipe.Stage`, 
    internally creating :class:`~mpipe.OrderedWorker` objects."""
    def __init__(self, target, size=1, disable_result=False):
        """Constructor takes a function implementing 
        :meth:`OrderedWorker.doTask`."""
        super(OrderedStage, self).__init__(_Worker, size, disable_result, task_fn=target)
