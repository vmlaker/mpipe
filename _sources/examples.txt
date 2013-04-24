.. _examples:

Examples
========

The sample codes in the following sections will show you the basics of building pipelines. The end functionality of these is trivial, and intended mainly to illustrate concepts of |NAME|. Feel free to run and experiment with the examples yourself. 

Getting started
---------------

.. toctree::

   examples1


Advanced topics
---------------

.. toctree::

   examples2

Expert techniques
-----------------

.. toctree::

   examples3

All examples have links to the source code on the right side above and below each code listing. In addition, all programs are located in the ``test/`` subdirectory of |NAME| distribution. 

When running the examples, keep in mind the multiprocessing nature of |NAME|, especially when running interactively from the Python interpreter (e.g. cut-and-pasting into the ``>>>`` prompt) -- some examples may display mangled text output, particularly in case of multiple processes simultaneously printing to stdout. For that reason, you may prefer to run the examples from your OS shell command prompt instead. If an example shows an actual command running a program, you can reproduce it by running the command from the root of the |NAME| distribution (directory that contains the ``test/`` subdirectory.)

.. the end.
