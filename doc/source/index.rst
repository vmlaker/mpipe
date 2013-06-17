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

|NAME| is a tiny Python module -- a thin layer above the standard :mod:`multiprocessing` package -- that lets you write multi-stage, multi-processing pipeline algorithms with remarkable ease. Consider the following workflow:

.. image:: tiny.png
   :align: center

It's a two-stage pipeline that increments and doubles numbers, each stage concurrently running three workers.
Here's how you'd code it up using the :mod:`mpipe` module:

.. literalinclude:: tiny.py

The above snippet runs a total of seven processes: one for the main program and six for the two stages (each stage running three workers.)

Installation
************

Get |NAME| now! Easiest way is using *pip*:
::

  pip install mpipe

Check out :doc:`download` for other ways of getting |NAME| up and running on your system. 

Got it, now what?
*****************

Start piping right away by running through the :doc:`examples`.
If you want a step-by-step guide to creating pipelines, read the :doc:`cookbook`.
For theory and design, take a look at :doc:`concepts`.
 
----

.. figure:: GitHub-Mark-64px.png
   :align: center
   :target: http://github.com/vmlaker/mpipe

   |NAME| is a `project on GitHub <http://github.com/vmlaker/mpipe>`_.
