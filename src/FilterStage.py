"""Implements FilterStage class."""

from .Stage import Stage
from .FilterWorker import FilterWorker

class FilterStage(Stage):
    """Single worker stage running 
    :class:`~mpipe.FilterWorker`."""
    def __init__(
        self, 
        stages, 
        max_tasks=1, 
        drop_results=False, 
        cache_results=False,
        do_stop_task=True,
        ):
        super(FilterStage, self).__init__(
            FilterWorker, 
            size=1, 
            do_stop_task=do_stop_task,
            stages=stages,
            max_tasks=max_tasks,
            drop_results=drop_results,
            cache_results=cache_results,
            )
