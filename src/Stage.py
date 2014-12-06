"""Implements Stage class."""

class Stage(object):
    """The Stage is an assembly of workers of identical functionality."""

    def __init__(
        self, 
        worker_class, 
        size=1,
        disable_result=False,
        do_stop_task=False, 
        input_tube=None,
        **worker_args
        ):
        """Create a stage of workers of given *worker_class* implementation, 
        with *size* indicating the number of workers within the stage.
        *disable_result* overrides any result defined in worker implementation,
        and does not propagate it downstream (equivalent to the worker
        producing ``None`` result).

        *do_stop_task* indicates whether the incoming "stop" signal (``None`` value)
        will actually be passed to the worker as a task. When using this option,
        implement your worker so that, in addition to regular incoming tasks,
        it handles the ``None`` value as well. This will be
        the worker's final task before the process exits.

        Any worker initialization arguments are given in *worker_args*."""
        self._worker_class = worker_class
        self._worker_args = worker_args
        self._size = size
        self._disable_result = disable_result
        self._do_stop_task = do_stop_task
        self._input_tube = self._worker_class.getTubeClass()() \
                           if not input_tube else input_tube
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

    def results(self):
        """Return a generator to iterate over results from the stage."""
        while True:
            result = self.get()
            if result is None: break
            yield result

    def link(self, next_stage):
        """Link to the given downstream stage *next_stage*
        by adding its input tube to the list of this stage's output tubes.
        Return this stage."""
        if next_stage is self: raise ValueError('cannot link stage to itself')
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
        # is at the end of a fork (hasn't been linked to any stage downstream).
        # Therefore, create one output tube.
        if not self._output_tubes:
            self._output_tubes.append(self._worker_class.getTubeClass()())

        self._worker_class.assemble(
            self._worker_args,
            self._input_tube,
            self._output_tubes,
            self._size,
            self._disable_result,
            self._do_stop_task,
            )

        # Build all downstream stages.
        for stage in self._next_stages:
            stage.build()
