"""Implements FilterWorker class."""

import sys
from .OrderedWorker import OrderedWorker
from .Pipeline import Pipeline

class FilterWorker(OrderedWorker):
    """FilterWorker filters input to sub-pipelines."""

    def __init__(self, stages, max_tasks=1, drop_results=False, cache_results=False):
        """Constructor takes an iterable of
        :class:`~mpipe.Stage` 
        objects and creates one pipeline for each stage.
        The filter then propagates its input task as input into each pipeline,
        filtered by limiting the number of tasks allowed in the stream of a pipeline,
        given as *max_tasks* parameter. Any task in excess is not added to
        a topped-out pipeline.

        For every input task (even tasks not propagated to sub-pipelines)
        the filter stage produces a result.
        By default, as its result, the filter stage produces a tuple (task, results) 
        where results is a list of results from all pipelines, 
        unless *drop_results* is True, in which case it ignores any 
        sub-pipeline result, and propagates only the input task.

        If *drop_results* is False, then *cache_results* flag may be used
        to save (i.e. cache) last results from pipelines. These are then 
        used as repeated pipeline results when a pipeline does not produce
        a result upon the current input task.        
        """

        # Create a pipeline out of each stage.
        self._pipelines = list()
        self._task_counts = dict()  # Maintain counts of tasks in pipes.
        for stage in stages:
            pipe = Pipeline(stage)
            self._pipelines.append(pipe)
            self._task_counts[pipe] = 0  # Initilize the task count.

        self._max_tasks = max_tasks  
        self._drop_results = drop_results
        self._cache_results = cache_results

        # Maintain a table of last results from each pipeline.
        self._last_results = dict()  

    def doTask(self, task):
        """Filter input *task* to pipelines -- make sure each one has no more
        than *max_tasks* tasks in it. Return a tuple
          (*task*, *results*)
        where *task* is the given task, and *results* is 
        a list of latest retrieved results from pipelines."""

        # If we're not caching, then clear the table of last results.
        if not self._cache_results:
            self._last_results = dict()

        # Iterate the list of pipelines, draining each one of any results.
        # For pipelines whose current stream has less than *max_tasks* tasks 
        # remaining, feed them the current task.
        for pipe in self._pipelines:

            count = self._task_counts[pipe]

            # Let's attempt to drain all (if any) results from the pipeline.
            valid = True
            last_result = None
            while count and valid:
                valid, result = pipe.get(sys.float_info.min)
                if valid:
                    last_result = result
                    count -= 1

            # Unless we're dropping results, save the last result (if any).
            if not self._drop_results:
                if last_result is not None:
                    self._last_results[pipe] = last_result

            # If there is room for the task, or if it is a "stop" request,
            # put it on the pipeline.
            if count <= self._max_tasks-1 or task is None:
                pipe.put(task)
                count += 1

            # Update the task count for the pipeline.
            self._task_counts[pipe] = count

        # If we're only propagating the task, do so now.
        if self._drop_results:
            return task

        # Otherwise, also propagate the assembly of pipeline results.
        all_results = [res for res in self._last_results.values()]
        return task, all_results
