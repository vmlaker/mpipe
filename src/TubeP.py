"""Implements TubeP class."""

import multiprocessing

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
