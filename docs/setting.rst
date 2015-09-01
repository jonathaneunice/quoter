Cloning and Setting
===================

``Quoter`` parameters can be changed (set) in real time.::

    bars = Quoter('|')
    print bars('x')                    # |x|
    bars.set(prefix='||', suffix='||')
    print bars('x')                    # ||x||
    bars.set(padding=1)
    print bars('x')                    # || x ||

And ``Quoter`` instances you like can be cloned, optionally with several
options changed in the clone::

    bart = bars.clone(prefix=']', suffix='[')
    assert bart('x') == '] x ['

