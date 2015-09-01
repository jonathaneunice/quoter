from quoter import *
import pytest


def test_md_basic():
    assert md.i('this') == '*this*'
    assert md.b('that') == '**that**'
    assert md.a('CNN', 'http://www.cnn.com') == \
                "[CNN](http://www.cnn.com)"


def test_md_h():
    assert md.h('title')    == "# title"
    assert md.h('title', 1) == "# title"
    assert md.h('title', 2) == "## title"
    assert md.h('title', 3) == "### title"
    assert md.h('title', 4) == "#### title"

    # test close
    assert md.h('title',    close=True) == "# title #"
    assert md.h('title', 1, close=True) == "# title #"
    assert md.h('title', 2, close=True) == "## title ##"
    assert md.h('title', 3, close=True) == "### title ###"
    assert md.h('title', 4, close=True) == "#### title ####"

    # test setext
    assert md.h('title',    setext=True) == "title\n=====\n"
    assert md.h('title', 1, setext=True) == "title\n=====\n"
    assert md.h('title', 2, setext=True) == "title\n-----\n"
    assert md.h('title', 3, setext=True) == "title\n-----\n"
    assert md.h('title', 4, setext=True) == "title\n-----\n"


def test_md_p():
    assert md.p('this') == 'this'
    assert md.p('this ', md.i('and'), ' that') == 'this *and* that'
    assert md.p('some other stuff') == 'some other stuff'


def test_md_doc():
    paras = [md.p('this ', md.i('and'), ' that'),
             md.p('some other stuff')]
    assert md.doc(paras) == \
           'this *and* that\n\nsome other stuff\n'

@pytest.mark.xfail
def test_md_hr():
    assert md.hr() == "----"

    assert md.doc([md.p("one"), md.hr(), md.p("two")]) == \
                "one\n\n----\n\ntwo\n"

# FIXME: hr fails to basic style defn problem 