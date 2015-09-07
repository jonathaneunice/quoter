

from quoter.styleset import *
from quoter import *
import pytest


def test_basic():

    s = StyleSet(Quoter)
    s.braces = braces

    assert s.braces('this') == '{this}'


def test_setattr():
    s = StyleSet(Quoter)

    s.bspace = braces.but(padding=1)
    assert s.bspace('that') == '{ that }'


def test_getitem():
    s = StyleSet(Quoter)
    s.braces = braces

    assert s['braces'] is braces
    assert s['braces']('curly') == '{curly}'


def test_setitem():
    s = StyleSet(Quoter)
    s['braces'] = braces

    assert s['braces'] is braces
    assert s.braces is braces
    assert s['braces']('curly') == '{curly}'
    assert s.braces('curly') == '{curly}'


def test_getattr_and_definition_not_instant():
    s = StyleSet(Quoter)

    s._define("db", "{{", "}}")
    assert s.db("work") == "{{work}}"

    with pytest.raises(ValueError):
        s.dbspace("{{ ", " }}")("works")

    s._define("wook", prefix="WO", suffix="OK")
    assert s.wook('this') == "WOthisOK"


def test_getattr_factory_instant():

    h = StyleSet(HTMLQuoter, instant=True)
    assert h.pre('this', ".work") == "<pre class='work'>this</pre>"
    assert h.free('open source', ".liberty") == \
        "<free class='liberty'>open source</free>"


def test_immediate():
    q = StyleSet(immediate=brackets)
    assert q("this") == '[this]'

    qnone = StyleSet()
    with pytest.raises(KeyError):
        qnone("this")


def test_repr():
    s = StyleSet()
    s.a = 1
    s['b'] = 2
    assert repr(s) in [ 'StyleSet(a=1, b=2)', 'StyleSet(b=2, a=1)']


def test_examples():
    """
    Test examples from the docs
    """

    colon = quote._define('colon', ':')
    assert colon('this') == quote.colon('this') == ':this:'

    assert quote("super") == "'super'"

    cq = StyleSet(factory=Quoter,
                  immediate=Quoter(':'))

    cq._define("two", Quoter('::'))

    assert cq('this') == ':this:'
    assert cq.two('this') == '::this::'
