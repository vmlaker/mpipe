.. _fordevelopers:

For developers
==============

If you want to contribute to |NAME| development,
start by forking the `repo <https://github.com/vmlaker/mpipe>`_.
After making changes to the code, run the build/test cycle
as shown in the developer guide below.

Build/install/test
------------------

It's recommended you use Python Virtualenv for your build/test cycle.
A good place to install Virtualenv is in the root project directory, 
simply by running:
::

   virtualenv venv

Use *Distutils* to build the code:
::

   venv/bin/python setup.py build

Install into your Virtualenv Python:
::

   venv/bin/python setup.py install

Run all tests:
::

   venv/bin/python setup.py test

Update Pypi
-----------

To update the Python Package Index, run:
::

   venv/bin/python setup.py clean build sdist upload

Build docs
----------

To build |NAME| documentation,
go to ``doc`` directory and take a look at
``create-gh-pages.sh`` script. 

.. End of file.
