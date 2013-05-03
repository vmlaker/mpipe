.. _index:

.. toctree::
   :hidden:

   docs
   download
   concepts
   cookbook
   examples
   api
   about

Welcome!
********

|NAME| is a Python library that lets you easily write multi-stage, multiprocess pipeline algorithms. Consider a two-stage pipeline that increments and doubles numbers, each stage concurrently running three workers. Something like this:

.. image:: tiny.png
   :align: center

Using the |NAME| module, you would write it like this:

.. literalinclude:: tiny.py

The above code runs a total of seven processes: one for the main program and six for the two stages (each stage running three workers.)

Installation
************

Start using |NAME| now! Easiest way is using pip:
::

  pip install --user mpipe

For other ways of getting |NAME| installed on your system, check out :doc:`download`.

Ok, now what?
*************

Start piping right away by running the :doc:`examples`.
Read the :doc:`cookbook` for a step-by-step guide to creating pipelines.
For theory and design, take a look at :doc:`concepts`.

.. The end.
