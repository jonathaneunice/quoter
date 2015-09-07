Shortcuts
=========

One often sees very long function calls and expressions as text parts are being
assembled. In order to reduce this problem, ``quoter`` defines aliases for
``single``, ``double``, and ``triple`` quoting, as well as ``backticks``, and
double backticks::

    from quoter import qs, qd, qt, qb, qdb

    print qs('one'), qd('two'), qt('three'), qb('and'), qdb('four')
    # 'one' "two" """three""" `and` ``four``

You can, of course, define your own aliases as well, and/or redefine existing
styles. If, for example, you like ``braces`` but wish it added a padding space
by default, it's simple to redefine::

    sbraces = Quoter('{', '}', padding=1)
    print sbraces('braces plus spaces!')  # '{ braces plus spaces! }'

You could alternatively riff off of the existing ``braces``::

    sbraces = braces.but(padding=1)

You could still get the no-padding variation with::

    print braces('no space braces', padding=0) # '{no space braces}'


