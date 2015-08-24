Change Log
==========

Version 1.5.2 (August 23, 2015)
'''''''''''''''''''''''''''''''

* Starts automatic collection of test branch coverage. Begins with 99%
  coverage.


Version 1.5.0 (August 20, 2015)
'''''''''''''''''''''''''''''''

* Enables cloning and specialization of all ``Quoter`` subclasses,
  including ``xml`` and ``html`` objects docs previously warned were
  non-functional. Refactors majority of ``Joiner`` functionality as a
  subclass of ``Quoter``, with all the rights and privileges thereunto
  appertaining.

* Extends tests.


Version 1.4.4 (August 20, 2015)
'''''''''''''''''''''''''''''''

* Added "naked" invocations of primary quoter front-ends, such as
  ``html("joe", "b.one")``. This allows quoters to take on primary
  information (such as the tag name) during each call.  This was long
  planned for the API, but had been sidelined due to now-quashed
  complexity.


Version 1.4.3 (August 20, 2015)
'''''''''''''''''''''''''''''''

* Added ``but`` synonym for ``clone`` to have simpler, clearer
  invocations.


Version 1.4.2 (August 20, 2015)
'''''''''''''''''''''''''''''''

* Docs were getting long. Truncated ``README.rst`` and converted
  majority to Sphinx docs to be hosted on readthedocs.


Version 1.4.1 (August 20, 2015)
'''''''''''''''''''''''''''''''

* Documentation fix.


Version 1.4.0 (August 20, 2015)
'''''''''''''''''''''''''''''''

* Major rewrite of complex argument handling for XMLQuoter (and
  HTMLQuoter subclass). Should be much more robust and extensible.
  Refactored some functions into ``util.py``

* Adds direct attribute setting ``[key=value]`` to the CSS selector
  specification language.

* Improved testing. Added new tests of sub-cases of parsing the
  arguments. Updated strategy to have quicker basic tests with ``sudo
  tox``, but easy full coverage analysis with  ``sudo tox -c
  toxcov.ini``. Advances test line coverage to 100%.


Version 1.3.6 (August 17, 2015)
'''''''''''''''''''''''''''''''

* Updated testing strategy with integrated multi-version coverage
  testing. Achieved 98%.


Version 1.3.5 (August 14, 2015)
'''''''''''''''''''''''''''''''

* Fixed RST problem in docs


Version 1.3.4 (August 14, 2015)
'''''''''''''''''''''''''''''''

* Added Travis CI badge and note about 2.6 release to docs


Version 1.3.3 (August 11, 2015)
'''''''''''''''''''''''''''''''

* Some code reorganization and updating of common string routines.


Version 1.3.2 (August 11, 2015)
'''''''''''''''''''''''''''''''

* Initiated external CI with Travis. Dropped Python 2.6 from official
  support given issues getting it running on Travis (though it
  actually does work).


Version 1.3.0 (August 11, 2015)
'''''''''''''''''''''''''''''''

* First release of integrated sequence joining. ``join``,
  ``word_join``, ``and_join``, ``or_join``, ``joinlines``, and
  ``items`` are functional and tested, but still less mature than the
  rest of the codebase.


Version 1.2.0 (August 11, 2015)
'''''''''''''''''''''''''''''''

* Institutes full named styles within each quoting class. Tests and
  docs tweaked. Embedded ``nulltype`` module withdrawn in favor of
  full ``nulltype`` imported by ``options``.


Version 1.1.4 (August 3, 2015)
''''''''''''''''''''''''''''''

* Experimental switch to YAML format for change log. Some setup,
  testing, and config updates.


Version 1.1.3 (August 3, 2015)
''''''''''''''''''''''''''''''

* Cloning and changing of ``Quoter`` instances (though not yet
  ``HTMLQuoter`` or ``XMLQuoter`` instances) is now operational.


Version 1.1.0 (August 3, 2015)
''''''''''''''''''''''''''''''

* Cleans up HTML quoting, esp. re void / self-closing elements. Adds
  new double-backtick functions. Changed to Apache License 2.0.
  Updates docs and testing matrix.


Version 1.0.3 (November 1, 2013)
''''''''''''''''''''''''''''''''

* HTML, XML, and lambda quoters now use class-relative styles
  dictionaries, as opposed to piggybacking the standard Quoter styles
  dictionary.

* Improved docs and tests.

* Added ``lambdaq`` front-end parallel to ``quote``, ``html``, and
  ``xml``.


Version 1.0.2 (October 31, 2013)
''''''''''''''''''''''''''''''''

* Some internal cleanups to improve code reuse among classes. Bumped
  from Alpha to Beta status.


Version 1.0.1 (October 31, 2013)
''''''''''''''''''''''''''''''''

* A new alternate API consisting of attribute names off of a default
  quoting object (e.g. ``quote.single`` as a specialization of
  ``quote``) has been instituted. This is mostly, but not perfectly, a
  superset of the previous use of a ``quote()`` function.

* The naming infrastructure has been beefed up, with multiple names
  (aliases) possible for all named objects.

* A new ``XMLQuoter`` is inserted as a superclass of ``HTMLQuoter`. It
  has ``HTMLQuoter``'s ability to parse CSS style id and class name
  definitions (e.g. ``'#first.big.special'``), as well as namespace
  support (new ``ns`` attribute).

* XML and HTML quoters for individual tags are automagically generated
  upon first use. E.g. ``html.b('this')`` creates an
  ``HTMLQuoter(tag='b', name='b')`` quoter that is cached as
  ``html.b`` for subsequent uses.

* Updated versioning strategy to comply with `PEP 386
  <http://www.python.org/dev/peps/pep-0386/>`_

* Various other structural and packaging cleanups. E.g. moved into
  proper Python package; given introspectable version number; removed
  old ``verno`` auto-update of version number; this proper change long
  instituted; etc.


Version 0.308 (October 30, 2012)
''''''''''''''''''''''''''''''''

* Last version before PEP 386 versioning switch. Upgrade away from
  these old versions if for no other reason than improving the auto-
  install logic.



