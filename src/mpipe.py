"""MPipe is a multiprocessing pipeline software framework in Python."""

import sys
import multiprocessing

__version__ = '1.0.5'

class TubeP:
    """A unidirectional communication channel 
    using :class:`multiprocessing.Connection` for underlying implementation."""

    def __init__(self):
        (self._conn1, 
         self._conn2) = multiprocessing.Pipe(duplex=False)

    def put(self, data):
        """Put an item on the tube."""
        self._conn2.send(data)

    def get(self, timeout=None):
        """Return the next available item from the tube.

        Blocks if tube is empty, until a producer for the tube puts an item on it."""
        if timeout:
            # Todo: Consider locking the poll/recv block.
            # Otherwise, this method is not thread safe.
            if self._conn1.poll(timeout):
                return (True, self._conn1.recv())
            else:
                return (False, None)
        return self._conn1.recv()

class TubeQ:
    """A unidirectional communication channel 
    using :class:`multiprocessing.Queue` for underlying implementation."""

    def __init__(self):
        self._queue = multiprocessing.Queue()

    def put(self, data):
        """Put an item on the tube."""
        self._queue.put(data)

    def get(self, timeout=None):
        """Return the next available item from the tube.

        Blocks if tube is empty, until a producer for the tube puts an item on it."""
        if timeout:
            try:
                result = self._queue.get(True, timeout)
            except multiprocessing.Queue.Empty:
                return(False, None)
            return(True, result)
        return self._queue.get()


class OrderedWorker(multiprocessing.Process):
    """An OrderedWorker object operates in a stage where the order 
    of output results always matches that of corresponding input tasks.

    A worker is linked to its two nearest neighbors -- the previous 
    worker and the next -- all workers in the stage thusly linked 
    in circular fashion. 
    Input tasks are fetched in this order, and before publishing it's result, 
    a worker first waits for it's previous neighbor to do the same."""

    def __init__(self):
        pass

    def init2(
        self, 
        input_tube,    # Read task from the input tube.
        output_tubes,  # Send result on all the output tubes.
        num_workers,   # Total number of workers in the stage.
        do_stop_task,  # Whether to call doTask() on "stop" request.
        ):
        """Create a worker with *input_tube* and an iterable of *output_tubes*.
        The worker reads a task from *input_tube* and writes the result to *output_tubes*."""
        super(OrderedWorker, self).__init__()
        self._tube_task_input = input_tube
        self._tubes_result_output = output_tubes
        self._num_workers = num_workers

        # Serializes reading from input tube.
        self._lock_prev_input = None
        self._lock_next_input = None

        # Serializes writing to output tube.
        self._lock_prev_output = None
        self._lock_next_output = None

        self._do_stop_task = do_stop_task

    @staticmethod
    def getTubeClass():
        """Return the tube class implementation."""
        return TubeP

    @classmethod
    def assemble(cls, args, input_tube, output_tubes, size, do_stop_task=False):
        """Create, assemble and start workers.
        Workers are created of class *cls*, initialized with *args*, and given
        task/result communication channels *input_tube* and *output_tubes*.
        The number of workers created is according to *size* parameter.
        *do_stop_task* indicates whether doTask() will be called for "stop" request.
        """

        # Create the workers.
        workers = []
        for ii in range(size):
            worker = cls(**args)
            worker.init2(
                input_tube,
                output_tubes,
                size,
                do_stop_task,
                )
            workers.append(worker)

        # Connect the workers.
        for ii in range(size):
            worker_this = workers[ii]
            worker_prev = workers[ii-1]
            worker_prev._link(
                worker_this, 
                next_is_first=(ii==0),  # Designate 0th worker as the first.
                )

        # Start the workers.
        for worker in workers:
            worker.start()

    def _link(self, next_worker, next_is_first=False):
        """Link the worker to the given next worker object, 
        connecting the two workers with communication tubes."""

        lock = multiprocessing.Lock()
        next_worker._lock_prev_input = lock
        self._lock_next_input = lock
        lock.acquire()

        lock = multiprocessing.Lock()
        next_worker._lock_prev_output = lock
        self._lock_next_output = lock
        lock.acquire()

        # If the next worker is the first one, trigger it now.
        if next_is_first:
            self._lock_next_input.release()
            self._lock_next_output.release()

    def putResult(self, result, count=0):
        """Register the *result* by putting it on all the output tubes."""
        self._lock_prev_output.acquire()
        for tube in self._tubes_result_output:
            tube.put((result, count))
        self._lock_next_output.release()
        
    def run(self):

        # Run implementation's initialization.
        self.doInit()

        while True:
            try:
                # Wait on permission from the previous worker that it's 
                # okay to retrieve the input task.
                self._lock_prev_input.acquire()

                # Retrieve the input task.
                (task, count) = self._tube_task_input.get()

                # Give permission to the next worker that it's 
                # okay to retrieve the input task.
                self._lock_next_input.release()

            except:
                (task, count) = (None, 0)

            # In case the task is None, it represents the "stop" request,
            # the count being the number of workers in this stage that had
            # already stopped.
            if task is None:

                # If this worker is the last one (of its stage) to receive the 
                # "stop" request, propagate "stop" to the next stage. Otherwise,
                # maintain the "stop" signal in this stage for another worker that
                # will pick it up. 
                count += 1
                if count == self._num_workers:
                    
                    # Propagating the "stop" to the next stage does not require
                    # synchronization with previous and next worker because we're
                    # guaranteed (from the count value) that this is the last worker alive. 
                    # Therefore, just put the "stop" signal on the result tube.
                    for tube in self._tubes_result_output:
                        tube.put((None, 0))

                else:
                    self._tube_task_input.put((None, count))

                # In case we're calling doTask() on a "stop" request, do so now.
                if self._do_stop_task:
                    self.doTask(None)

                # Honor the "stop" request by exiting the process.
                break  

            # The task is not None, meaning that it's an actual task to
            # be processed. Therefore let's call doTask().
            result = self.doTask(task)

            # If doTask() actually returns a result (and the result is not None),
            # it indicates that it did not call putResult(), instead intending
            # it to be called now.
            if result is not None:
                self.putResult(result)

    def doTask(self, task):
        """Implement this method in the subclass to be executed for each task.
        The implementation can publish the output result in one of two ways: 
        1) either by calling :meth:`putResult` and returning ``None`` or
        2) by returning the result (other than ``None``.)"""
        return True

    def doInit(self):
        """Implement this method in the subclass, if there's need
        for any additional initialization upon process startup.
        This method is called after the worker process starts,
        and before it begins processing tasks."""
        return None


class UnorderedWorker(multiprocessing.Process):
    """An UnorderedWorker object operates independently of other
    workers in the stage, publishing it's result without coordinating
    with others. The order of output results may not match 
    that of corresponding input tasks."""

    def __init__(self):
        pass

    def init2(
        self, 
        input_tube,    # Read task from the input tube.
        output_tubes,  # Send result on all the output tubes.
        num_workers,   # Total number of workers in the stage.
        do_stop_task,  # Whether to call doTask() on "stop" request.
        ):
        """Create a worker with *input_tube* and an iterable of *output_tubes*.
        The worker reads a task from *input_tube* and writes the result to *output_tubes*."""
        super(UnorderedWorker, self).__init__()
        self._tube_task_input = input_tube
        self._tubes_result_output = output_tubes
        self._num_workers = num_workers
        self._do_stop_task = do_stop_task

    @staticmethod
    def getTubeClass():
        """Return the tube class implementation."""
        return TubeQ
    
    @classmethod
    def assemble(cls, args, input_tube, output_tubes, size, do_stop_task):
        """Create, assemble and start workers.
        Workers are created of class *cls*, initialized with *args*, and given
        task/result communication channels *input_tube* and *output_tubes*.
        The number of workers created is according to *size* parameter.
        *do_stop_task* indicates whether doTask() will be called for "stop" request.
        """

        # Create the workers.
        workers = []
        for ii in range(size):
            worker = cls(**args)
            worker.init2(
                input_tube,
                output_tubes,
                size,
                do_stop_task,
                )
            workers.append(worker)

        # Start the workers.
        for worker in workers:
            worker.start()

    def putResult(self, result, count=0):
        """Register the *result* by putting it on all the output tubes."""
        for tube in self._tubes_result_output:
            tube.put((result, count))

    def run(self):

        # Run implementation's initialization.
        self.doInit()

        while True:
            try:
                (task, count) = self._tube_task_input.get()
            except:
                (task, count) = (None, 0)

            # In case the task is None, it represents the "stop" request,
            # the count being the number of workers in this stage that had
            # already stopped.
            if task is None:

                # If this worker is the last one (of its stage) to receive the 
                # "stop" request, propagate "stop" to the next stage. Otherwise,
                # maintain the "stop" signal in this stage for another worker that
                # will pick it up. 
                count += 1
                if count == self._num_workers:
                    self.putResult(None)
                else:
                    self._tube_task_input.put((None, count))

                # In case we're calling doTask() on a "stop" request, do so now.
                if self._do_stop_task:
                    self.doTask(None)

                # Honor the "stop" request by exiting the process.
                break  

            # The task is not None, meaning that it's an actual task to
            # be processed. Therefore let's call doTask().
            result = self.doTask(task)

            # If doTask() actually returns a result (and the result is not None),
            # it indicates that it did not call putResult(), instead intending
            # it to be called now.
            if result is not None:
                self.putResult(result)

    def doTask(self, task):
        """Implement this method in the subclass to be executed for each task.
        The implementation can publish the output result in one of two ways: 
        1) either by calling :meth:`putResult` and returning ``None`` or
        2) by returning the result (other than ``None``.)"""
        return True

    def doInit(self):
        """Implement this method in the subclass, if there's need
        for any additional initialization upon process startup.
        This method is called after the worker process starts,
        after the worker process starts,
        and before it begins processing tasks."""
        return None


class Stage(object):
    """The Stage is an assembly of workers of identical functionality."""

    def __init__(self, worker_class, size=1, do_stop_task=False, **worker_args):
        """Create a stage of workers of given *worker_class* implementation, 
        with *size* indicating the number of workers within the stage.
        *do_stop_task* indicates whether the worker's doTask() method will be
        called on a "stop" (i.e. None) task.
        Any worker initialization arguments are given in *worker_args*."""
        self._worker_class = worker_class
        self._worker_args = worker_args
        self._size = size
        self._do_stop_task = do_stop_task
        self._input_tube = self._worker_class.getTubeClass()()
        self._output_tubes = list()
        self._next_stages = list()

    def put(self, task):
        """Put *task* on the stage's input tube."""
        self._input_tube.put((task,0))

    def get(self, timeout=None):
        """Retrieve results from all the output tubes."""
        valid = False
        result = None
        for tube in self._output_tubes:
            if timeout:
                valid, result = tube.get(timeout)
                if valid:
                    result = result[0]
            else:
                result = tube.get()[0]
        if timeout:
            return valid, result
        return result

    def link(self, next_stage):
        """Link to the given downstream stage *next_stage*
        by adding it's input tube to the list of this stage's output tubes.
        Return this stage."""
        self._output_tubes.append(next_stage._input_tube)
        self._next_stages.append(next_stage)
        return self

    def getLeaves(self):
        """Return the downstream leaf stages of this stage."""
        result = list()
        if not self._next_stages:
            result.append(self)
        else:
            for stage in self._next_stages:
                leaves = stage.getLeaves()
                result += leaves
        return result

    def build(self):
        """Create and start up the internal workers."""

        # If there's no output tube, it means that this stage
        # is at the end of a fork (hasn't been linked to any stage downstream.)
        # Therefore, create one output tube.
        if not self._output_tubes:
            self._output_tubes.append(self._worker_class.getTubeClass()())

        self._worker_class.assemble(
            self._worker_args,
            self._input_tube,
            self._output_tubes,
            self._size,
            self._do_stop_task,
            )

        # Build all downstream stages.
        for stage in self._next_stages:
            stage.build()


class OrderedStage(Stage):
    """A specialized :class:`~mpipe.Stage`, 
    internally creating :class:`~mpipe.OrderedWorker` objects."""
    def __init__(self, target, size=1):
        """Constructor takes a function implementing 
        :meth:`OrderedWorker.doTask`."""
        class wclass(OrderedWorker):
            def doTask(self, task):
                return target(task)
        super(OrderedStage, self).__init__(wclass, size)


class UnorderedStage(Stage):
    """A specialized :class:`~mpipe.Stage`, 
    internally creating :class:`~mpipe.UnorderedWorker` objects."""
    def __init__(self, target, size=1):
        """Constructor takes a function implementing
        :meth:`UnorderedWorker.doTask`."""
        class wclass(UnorderedWorker):
            def doTask(self, task):
                return target(task)
        super(UnorderedStage, self).__init__(wclass, size)


class Pipeline(object):
    """A pipeline of stages."""
    def __init__(self, input_stage):
        """Constructor takes the root upstream stage."""
        self._input_stage = input_stage
        self._output_stages = input_stage.getLeaves()
        self._input_stage.build()

    def put(self, task):
        """Put *task* on the pipeline."""
        self._input_stage.put(task)

    def get(self, timeout=None):
        """Return result from the pipeline."""
        result = None
        for stage in self._output_stages:
            result = stage.get(timeout)
        return result

    def results(self):
        """Return a generator to iterate over results from the pipeline."""
        while True:
            result = self.get()
            if result is None: break
            yield result


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

            # Unless we're dropping results, save the last result (if any.)
            if not self._drop_results:
                if last_result is not None:
                    self._last_results[pipe] = last_result

            # If there is room for the task, or if it's a "stop" request,
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

# The end.
