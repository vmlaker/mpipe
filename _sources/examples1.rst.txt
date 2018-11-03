.. _examples1:

.. _hello_world:

Hello world
-----------

Let's start with a really simple workflow, a "hello world" of pipelines if you will.

.. image:: helloworld.png
   :align: center

It just prints each input element as it comes in. Feeding it a stream of numbers 0, 1, 2, 3 simply echoes the numbers to your terminal's standard output. Here's the code:

.. container:: source-click-above

  [`source <helloworld.py>`_]

.. literalinclude:: helloworld.py

.. container:: source-click-below

  [`source <helloworld.py>`_]

The program output is:
::

  0
  1
  2
  3
 
It's a silly pipeline that doesn't do much other than illustrate a few basic ideas. Note the last line that puts ``None`` on the pipeline -- this sends the "stop" task, effectively signaling all processes within the pipeline to terminate.

.. _serializing_stages:

Serializing stages
------------------

Multiple stages can be serially linked to create a sequential workflow:

.. image:: chain.png
   :align: center

.. container:: source-click-above

  [`source <chain.py>`_]

.. literalinclude:: chain.py

.. container:: source-click-below

  [`source <chain.py>`_]

.. _pipeline_with_output:

Pipeline with output
--------------------

Have you noticed that the pipelines so far did not actually produce results at the output end? Here's a pipeline similar to the previous one, except that the final result is returned as *pipeline output* instead of being passed to a third stage:

.. image:: pipeout.png
   :align: center

Without a third stage doing the printing, the caller of the pipeline must print the final result:

.. container:: source-click-above

  [`source <pipeout.py>`_]

.. literalinclude:: pipeout.py

.. container:: source-click-below

  [`source <pipeout.py>`_]

Note that, before fetching results, we need to put the "stop" task on the pipeline. That's because :meth:`~mpipe.Pipeline.results()` returns a generator function that continues to fetch results so long as the pipeline remains alive. Without previously signaling "stop", the fetch loop would hang on the fifth iteration.

Another way to fetch results is to call :meth:`~mpipe.Pipeline.get()` exactly four times. Using this method it doesn't matter whether you signal "stop" before or after the fetch loop:
::

  for foobar in range(10):
     print(pipe.get())
 
  pipe.put(None)


.. _forked_pipeline:

Forked pipeline
---------------

Imagine a pipeline that forks into two separate flows of execution:

.. image:: fork.png
   :align: center

We can fork into more than two paths, but let's keep it simple for now.

.. container:: source-click-above

  [`source <fork.py>`_]

.. literalinclude:: fork.py

.. container:: source-click-below

  [`source <fork.py>`_]

This time instead of using standalone functions to implement the work, we used classes. It's really the same thing, but with classes you have greater potential for encapsulation and code organization when implementing complex stages. Note that this requires a slightly different way of creating stage objects, now using the :mod:`~mpipe.Stage` class.

.. the end
