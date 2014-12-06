"""Implements UnorderedWorker class."""

import multiprocessing
from .TubeQ import TubeQ

class UnorderedWorker(multiprocessing.Process):
    """An UnorderedWorker object operates independently of other
    workers in the stage, fetching the first available task, and
    publishing its result whenever it is done
    (without coordinating with neighboring workers).
    Consequently, the order of output results may not match 
    that of corresponding input tasks."""

    def __init__(self):
        pass

    def init2(
        self, 
        input_tube,      # Read task from the input tube.
        output_tubes,    # Send result on all the output tubes.
        num_workers,     # Total number of workers in the stage.
        disable_result,  # Whether to override any result with None.
        do_stop_task,    # Whether to call doTask() on "stop" request.
        ):
        """Create *num_workers* worker objects with *input_tube* and 
        an iterable of *output_tubes*. The worker reads a task from *input_tube* 
        and writes the result to *output_tubes*."""

        super(UnorderedWorker, self).__init__()
        self._tube_task_input = input_tube
        self._tubes_result_output = output_tubes
        self._num_workers = num_workers
        self._disable_result = disable_result
        self._do_stop_task = do_stop_task

    @staticmethod
    def getTubeClass():
        """Return the tube class implementation."""
        return TubeQ
    
    @classmethod
    def assemble(
        cls, 
        args, 
        input_tube, 
        output_tubes, 
        size, 
        disable_result,
        do_stop_task,
        ):
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
                disable_result,
                do_stop_task,
                )
            workers.append(worker)

        # Start the workers.
        for worker in workers:
            worker.start()

    def putResult(self, result):
        """Register the *result* by putting it on all the output tubes."""
        for tube in self._tubes_result_output:
            tube.put((result, 0))

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

            # The task is not None, meaning that it is an actual task to
            # be processed. Therefore let's call doTask().
            result = self.doTask(task)

            # Unless result is disabled,
            # if doTask() actually returns a result (and the result is not None),
            # it indicates that it did not call putResult(), instead intending
            # it to be called now.
            if not self._disable_result and result is not None:
                self.putResult(result)

    def doTask(self, task):
        """Implement this method in the subclass with work
        to be executed on each *task* object.
        The implementation can publish the output result in one of two ways,
        either by 1) calling :meth:`putResult` and returning ``None``, or
        2) returning the result (other than ``None``)."""
        return True

    def doInit(self):
        """Implement this method in the subclass in case there's need
        for additional initialization after process startup.
        Since this class inherits from :class:`multiprocessing.Process`,
        its constructor executes in the spawning process.
        This method allows additional code to be run in the forked process,
        before the worker begins processing input tasks.
        """
        return None
