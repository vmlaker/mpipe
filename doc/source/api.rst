.. _api:

**********
|NAME| API
**********

.. module:: mpipe

.. autoclass:: mpipe.OrderedWorker
   :members: doTask, putResult

.. autoclass:: mpipe.UnorderedWorker
   :members: doTask, putResult

.. autoclass:: mpipe.Stage
   :members: link, put, get

.. autoclass:: mpipe.OrderedStage
   :members:

.. autoclass:: mpipe.UnorderedStage
   :members:

.. autoclass:: mpipe.Pipeline
   :members: put, get, results

.. autoclass:: mpipe.TubeP
   :members: put, get

.. autoclass:: mpipe.TubeQ
   :members: put, get

.. The end.
