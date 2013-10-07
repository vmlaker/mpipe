"""Implements UnorderedStage class."""

from .Stage import Stage

class UnorderedStage(Stage):
    """A specialized :class:`~mpipe.Stage`, 
    internally creating :class:`~mpipe.UnorderedWorker` objects."""
    def __init__(self, target, size=1, disable_result=False):
        """Constructor takes a function implementing
        :meth:`UnorderedWorker.doTask`."""
        class wclass(UnorderedWorker):
            def doTask(self, task):
                return target(task)
        super(UnorderedStage, self).__init__(wclass, size, disable_result)
