.. _api:

**********
|NAME| API
**********

.. module:: mpipe

.. autoclass:: mpipe.OrderedWorker
   :members: doTask, doInit, putResult

.. autoclass:: mpipe.UnorderedWorker
   :members: doTask, doInit, putResult

----

.. autoclass:: mpipe.Stage
   :members: link, put, get

.. autoclass:: mpipe.OrderedStage
   :members:

.. autoclass:: mpipe.UnorderedStage
   :members:

----

.. autoclass:: mpipe.Pipeline
   :members: put, get, results

----

.. autoclass:: mpipe.FilterWorker

.. autoclass:: mpipe.FilterStage

.. End of file.
