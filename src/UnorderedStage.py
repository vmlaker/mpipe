"""Implements UnorderedStage class."""

from .Stage import Stage
from .UnorderedWorker import UnorderedWorker
from .TubeQ import TubeQ

class UnorderedStage(Stage):
    """A specialized :class:`~mpipe.Stage`, 
    internally creating :class:`~mpipe.UnorderedWorker` objects."""
    def __init__(self, target, size=1, disable_result=False, max_backlog=None):
        """Constructor takes a function implementing
        :meth:`UnorderedWorker.doTask`."""
        class wclass(UnorderedWorker):
            def doTask(self, task):
                return target(task)
        super(UnorderedStage, self).__init__(wclass, size, disable_result,
                                             input_tube=TubeQ(maxsize=max_backlog) if max_backlog else None)
