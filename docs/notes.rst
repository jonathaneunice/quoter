Notes
=====

* ``quoter`` provides simple transformations that could be alternatively
  implemented as a series of small functions. The problem is that
  such "little functions" tend to be constantly re-implemented, in
  different ways, and spread through many programs. That need to
  constantly re-implement such common tasks has led me to re-think
  how software should construct text on a grander scale.  ``quoter``
  is one facet of a project to systematize higher-level formatting
  operations. See `say <http://pypi.python.org/pypi/say>`_ and `show
  <http://pypi.python.org/pypi/show>`_ for other parts of the larger
  effort.

* ``quoter`` is a test case for, and leading user of, `options
  <http://pypi.python.org/pypi/options>`_, a module that supports flexible
  option handling. In some ways it is ``options`` most extensive test
  case, in terms of subclassing and dealing with named styles.

* In the future, additional quoting styles might appear.
  There is already (limited, experimental) support for Markdown,
  and other languages such as RST are straightforward.  It's not
  hard to subclass ``Quoter`` for new languages. Some of the things
  learned in the ``say`` project about text block management
  (indentation, wrapping, and such) are highly applicable to the
  quoting mission.

* You might look at some of the modules for ANSI-coloring text such as
  `ansicolors <https://pypi.python.org/pypi/ansicolors>`_ as being
  special cases of the ``quoter`` idea.  While ``quoter`` doesn't
  provide this specific kind of wrapping, it's in-line with the mission.

* Automated multi-version testing managed with the wonderful
  `pytest <http://pypi.python.org/pypi/pytest>`_,
  `pytest-cov <http://pypi.python.org/pypi/pytest-cov>`_,
  `coverage <http://pypi.python.org/pypi/coverage>`_,
  and `tox <http://pypi.python.org/pypi/tox>`_.
  Continuous integration testing
  with `Travis-CI <https://travis-ci.org/jonathaneunice/textdata>`_.
  Packaging linting with `pyroma <https://pypi.python.org/pypi/pyroma>`_.

* Successfully packaged for, and
  tested against, all late-model versions of Python: 2.6, 2.7, 
  3.3, 3.4, 3.5, and 3.6, as well as recent builds of PyPy 
  and PyPy3. 

* The author, `Jonathan Eunice <mailto:jonathan.eunice@gmail.com>`_ or
  `@jeunice on Twitter <http://twitter.com/jeunice>`_ welcomes your comments
  and suggestions.
