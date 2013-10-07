"""Implements Pipeline class."""

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
