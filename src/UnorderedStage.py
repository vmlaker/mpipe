"""Implements UnorderedStage class."""

from .Stage import Stage
from .UnorderedWorker import UnorderedWorker
from .TubeQ import TubeQ

__all__ = ['UnorderedStage']


class _Worker(UnorderedWorker):
    def __init__(self, task_fn):
        super(_Worker, self).__init__()
        self.task_fn = task_fn

    def doTask(self, task):
        return self.task_fn(task)


class UnorderedStage(Stage):
    """A specialized :class:`~mpipe.Stage`, 
    internally creating :class:`~mpipe.UnorderedWorker` objects."""
    def __init__(self, target, size=1, disable_result=False, max_backlog=None):
        """Constructor takes a function implementing
        :meth:`UnorderedWorker.doTask`."""
        super(UnorderedStage, self).__init__(_Worker, size, disable_result,
                                             input_tube=TubeQ(maxsize=max_backlog) if max_backlog else None,
                                             task_fn=target)
