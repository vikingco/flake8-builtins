Flake8 builtins plugin
======================

Check for overrides of Python builtin methods

This module provides a plugin for ``flake8``, the Python code checker.


Installation
------------

You can install or upgrade ``flake8-builtins-unleashed`` with these commands::

  $ pip install flake8-builtins-unleashed
  $ pip install --upgrade flake8-builtins-unleashed


Plugin for Flake8
-----------------

When both ``flake8`` and ``flake8-builtins-unleashed`` are installed, the plugin is
available in ``flake8``::

    $ flake8 --version
    2.0 (pep8: 1.4.5, flake8-builtins: 1.0, pyflakes: 0.6.1)

Options
-------

If you want to ignore a certain type of override, you can use the following option::

    $ flake8 --builtins-exclude=FloatingPointError,__import__
