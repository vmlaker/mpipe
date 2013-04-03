.. _index:

.. toctree::
   :hidden:

   docs
   concepts
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

Start using |NAME| now! Get the source code and install the module in the usual way:
::

  git clone https://github.com/vmlaker/mpipe
  cd mpipe
  python setup.py install --user

Next, check out :doc:`docs` and get ready to start piping in Python!

.. The end.
