.. _examples3:

.. _filtering:

Filtering
---------

If a stage can't process incoming tasks fast enough, we may have a bottleneck situation.
Imagine a stream of tasks feeding a pipeline at the rate of 10 tasks per second. 
A single-worker stage that only processes 8 tasks per second inevitably bottlenecks the workflow:

.. container:: source-click-above

  [`source <bottleneck1.py>`_]

.. literalinclude:: bottleneck1.py

.. container:: source-click-below

  [`source <bottleneck1.py>`_]

An easy way to fix this, of course, is to devote an additional worker to the stage:

.. container:: source-click-above

  [`source <bottleneck2.py>`_]

.. literalinclude:: bottleneck2.py

.. container:: source-click-below

  [`source <bottleneck2.py>`_]

But what if, for whatever reason, our design limits us to a single worker stage? 
If adding workers is not an option, we can instead choose to filter inputs into the problematic stage by dropping excess tasks:

.. container:: source-click-above

  [`source <bottleneck3.py>`_]

.. literalinclude:: bottleneck3.py

.. container:: source-click-below

  [`source <bottleneck3.py>`_]

Compare run times of the three programs above. Also, note the missing (dropped) task in output of the last program.

.. the end
