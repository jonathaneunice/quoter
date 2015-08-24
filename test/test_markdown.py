from quoter import *
import pytest


def test_md_basic():
    assert md.i('this') == '*this*'
    assert md.b('that') == '**that**'
    assert md.a('CNN', 'http://www.cnn.com') == \
                "[CNN](http://www.cnn.com)"


def test_md_p():
    assert md.p('this') == 'this'
    assert md.p('this ', md.i('and'), ' that') == 'this *and* that'
    assert md.p('some other stuff') == 'some other stuff'


def test_md_doc():
    paras = [md.p('this ', md.i('and'), ' that'),
             md.p('some other stuff')]
    assert md.doc(paras) == \
           'this *and* that\n\nsome other stuff\n'
