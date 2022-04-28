import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncPipeline(object):
    """ Async wrapper for a mpipe pipeline that allows for concurrent streams in
    and out via generator functions """

    def __init__(self, pipeline, data_source):
        self._pipeline = pipeline
        self._data_source = data_source
        self._executor = ThreadPoolExecutor(2)

    async def _pipe_filler(self):
        """ Async task to pass data from _data_source generator function into
        pipeline """
        for item in self._data_source():
            await self._loop.run_in_executor(
                self._executor,
                lambda: self._pipeline.put(item)
            )

        self._pipeline.put(None)

    async def start(self):
        """ Async generator method which starts the input stream into the 
        pipeline and yields result values from the pipeline """
        self._loop = asyncio.get_event_loop()
        self._loop.create_task(self._pipe_filler())
        while True:
            result = await self._loop.run_in_executor(
                self._executor, 
                self._pipeline.get
            )
            if result is None: break
            yield result
