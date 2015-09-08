

from quoter.util import *
import six
import pytest


def test_is_string():
    assert is_string("")
    assert is_string("This")
    assert is_string(six.u("this"))
    assert stringify(six.u("a\u2014b"))

    assert not is_string(1)
    assert not is_string(None)
    assert not is_string([1, 2, 3])
    assert not is_string(['a', 'b', 'c'])


def test_stringify():
    assert stringify('this') == 'this'
    assert stringify(4) == '4'
    assert stringify(six.u("\u2014")) == six.u("\u2014")


def test_is_sequence():
    assert not is_sequence('this')
    assert not is_sequence(six.u('this'))
    assert not is_sequence(4)
    assert not is_sequence(4.4)
    assert not is_sequence(3.3+2j)
    assert is_sequence([])
    assert is_sequence([1,3,4])
    assert is_sequence(set())
    assert is_sequence(set([1,3,4]))
    assert is_sequence(range(10))


def test_halfstr():
    assert halfstr("") == ["", ""]
    assert halfstr("[]") == ["[", "]"]
    assert halfstr("[[]]") == ["[[", "]]"]

    with pytest.raises(ValueError):
        halfstr("abc")

def test_listing():

    assert listing(None) == []

    assert listing(()) == []
    assert listing(('a',)) == ['a']
    assert listing(('a','b')) == ['a', 'b']
    assert listing(('a', 'b', 'c')) == ['a', 'b', 'c']

    assert listing([]) == []
    assert listing(['a']) == ['a']
    assert listing(['a','b']) == ['a', 'b']
    assert listing(['a', 'b', 'c']) == ['a', 'b', 'c']

    assert listing('') == []
    assert listing('a') == ['a']
    assert listing('a b') == ['a', 'b']
    assert listing('a b c') == ['a', 'b', 'c']


def test_blanknone():
    assert blanknone(None) == ''

    values = [0, 1, "", "this", True, False, list(range(4))]
    for v in values:
        assert blanknone(v) == v


def test_pad():
    assert pad([], 3) == [None, None, None]
    assert pad([1], 3) == [1, None, None]
    assert pad([1, 2], 3) == [1, 2, None]

    assert pad([], 3, -1) == [-1, -1, -1]
    assert pad([1], 3, -1) == [1, -1, -1]
    assert pad([1, 2], 3, -1) == [1, 2, -1]

    assert pad((), 3) == (None, None, None)
    assert pad((1,), 3) == (1, None, None)
    assert pad((1, 2), 3) == (1, 2, None)


def test_parse_css_selector():

    pcs = parse_css_selector

    assert pcs(None) == {}
    assert pcs("b") == { '_tag': 'b' }
    assert pcs("b.one") == { '_tag': 'b', 'class': 'one' }
    assert pcs("b.one.two") == { '_tag': 'b', 'class': 'one two' }
    assert pcs("b#name") == { '_tag': 'b', 'id': 'name' }
    assert pcs("b.one#name") == { '_tag': 'b', 'class': 'one', 'id': 'name' }
    assert pcs("b.one[andy=pandy]#name") == { '_tag': 'b', 'class': 'one',
                                              'id': 'name', 'andy': 'pandy' }


def test_combine_classes():


    cc = combine_classes
    assert cc(None, None) == None
    assert cc('one', None) == 'one'
    assert cc(None, 'two') == 'two'
    assert cc('one', 'two') == 'one two'
    assert cc('two', 'one') == 'two one'
    assert cc(None, 'billy idol') == 'billy idol'
    assert cc('billy jones', 'billy idol') == 'billy jones idol'
    assert cc('billy jones', 'idol billy billy nix') == 'billy jones idol nix'

    # simulate the reverse_classes setting
    cc = lambda x,y: combine_classes(y, x)
    assert cc(None, None) == None
    assert cc('one', None) == 'one'
    assert cc(None, 'two') == 'two'
    assert cc('one', 'two') == 'two one'
    assert cc('two', 'one') == 'one two'
    assert cc(None, 'billy idol') == 'billy idol'
    assert cc('billy jones', 'billy idol') == 'billy idol jones'
    assert cc('billy jones', 'idol billy billy nix') == 'idol billy nix jones'


def test_update_style_dict():
    d = { 'id': 'one' }
    update_style_dict(d, { 'class': 'billy idol'})
    assert d == { 'id': 'one', 'class': 'billy idol'}

    # first with simpler, non-class-reversing behavior
    d = { 'id': 'one', 'class': 'billy jones' }
    update_style_dict(d, { 'class': 'billy idol'}, reverse_class=False)
    assert d == { 'id': 'one', 'class': 'billy jones idol'}

    d = { 'id': 'one', 'class': 'billy jones' }
    update_style_dict(d, { 'class': 'idol billy billy nix',
                            'src': 'file.jpg' },
                      reverse_class=False)
    assert d == { 'id': 'one', 'class': 'billy jones idol nix',
                   'src': 'file.jpg' }


    # then with normal class-reversing behavior
    d = { 'id': 'one', 'class': 'billy jones' }
    update_style_dict(d, { 'class': 'billy idol'})
    assert d == { 'id': 'one', 'class': 'billy idol jones'}

    d = { 'id': 'one', 'class': 'billy jones' }
    update_style_dict(d, { 'class': 'idol billy billy nix',
                            'src': 'file.jpg' })
    assert d == { 'id': 'one', 'class': 'idol billy nix jones',
                   'src': 'file.jpg' }
