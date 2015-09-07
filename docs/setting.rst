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

The method ``but`` is a synonym for ``clone``. It is used to suggest
"I like everything there, but...change this and that."::

    bartwide = bart.but(margin=2)
    assert bartwide('x') == '  ] x [  '

Note that if any of the options for  ``bart`` besides ``margin`` change,
those changes will be reflected in ``bartwide`` as well. ``bartwide`` has
decided what its own margins will be, but delegated all other choices to
its parent object.