from quoter import *
import pytest


def test_braces():
    assert braces('this') == '{this}'
    assert braces('this', padding=1) == '{ this }'
    assert braces('this', margin=1) == ' {this} '
    assert braces('this', padding=1, margin=1) == ' { this } '


def test_brackets():
    assert brackets('this') == '[this]'
    assert brackets('this', padding=1) == '[ this ]'
    assert brackets('this', margin=1) == ' [this] '
    assert brackets('this', padding=1, margin=1) == ' [ this ] '

def test_other_named_ascii_styles():

    assert angles('this') == '<this>'
    assert parens('this') == '(this)'
    assert qs('this') == single('this') == "'this'"
    assert qd('this') == double('this') == '"this"'
    assert qt('this') == triple('this') == '"""this"""'
    assert qb('this') == backticks('this') == '`this`'
    assert qdb('this') == doublebackticks('this') == '``this``'

def test_named_unicode_styles():
    assert anglequote('this') == guillemet('this') == six.u('\u00abthis\u00bb')
    assert chevron('this') == six.u('\u2039this\u203a')
    assert curlysingle('this') == six.u('\u2018this\u2019')
    assert curlydouble('this') == six.u('\u201cthis\u201d')


def test_clone():
    """
    Make sure clones properly registered just like normally defined
    styles, that clones are different from original, that they yield
    the expected results, and that after cloning, the originals
    behave exactly as before
    """

    bar2 = quote.bar2 = brackets.clone(margin=2)
    assert bar2 is not brackets
    assert bar2('this') == '  [this]  '
    assert brackets('this') == '[this]'
    assert quote.bar2('this') == '  [this]  '

    bb = html.b.clone(padding=1, margin=2)
    assert bb is not html.b
    assert isinstance(html.b, HTMLQuoter)
    assert isinstance(bb, HTMLQuoter)
    assert bb('this') == '  <b> this </b>  '
    assert html.b('this') == '<b>this</b>'

    sp = html.b.but(atts='span')
    assert sp is not html.b
    assert sp('something') == '<span>something</span>'
    assert sp('else', '.other') == "<span class='other'>else</span>"


def test_but():
    """
    Test the but alias for clone.
    """
    bar2 = brackets.but(margin=2)
    assert bar2 is not brackets
    assert bar2('this') == '  [this]  '
    assert brackets('this') == '[this]'

    bb = html.b.but(padding=1, margin=2)
    assert bb is not html.b
    assert bb('this') == '  <b> this </b>  '
    assert html.b('this') == '<b>this</b>'


def test_set():
    bar2 = quote.bar2 = brackets.clone(margin=2)
    assert bar2('this') == '  [this]  '
    assert quote.bar2('this') == '  [this]  '
    # check that original object is not changed
    assert brackets('this') == '[this]'
    assert quote.brackets('this') == '[this]'

    # check setting options
    bar2.set(margin=1, padding=1)
    assert bar2('this') == ' [ this ] '
    assert quote.bar2('this') == ' [ this ] '
    # check that original object is not changed
    assert brackets('this') == '[this]'
    assert quote.brackets('this') == '[this]'

    # check setting options
    bar2.set(prefix='||', padding=1)
    assert bar2('this') == ' || this ] '
    assert quote.bar2('this') == ' || this ] '
    # check that original object is not changed
    assert brackets('this') == '[this]'
    assert quote.brackets('this') == '[this]'

def test_set_example():
    bars = Quoter('|')
    assert bars('x') == '|x|'
    bars.set(prefix='||', suffix='||')
    assert bars('x') == '||x||'
    bars.set(padding=1)
    assert bars('x') == '|| x ||'

    bart = bars.clone(prefix=']', suffix = '[')
    assert bart('x') == '] x ['

    bartwide = bart.but(margin=2)
    assert bartwide('x') == '  ] x [  '


@pytest.mark.skipif(True, reason='road closed')
def test_chars():
    percent = Quoter(chars='%%')
    assert percent('something') == '%something%'
    doublea = Quoter(chars='<<>>')
    assert doublea('AAA') == '<<AAA>>'

# From a quoter point of view, the chars kwarg is totally gilding the
# lily, and unnecessary. But from the point of view of exploring and
# exercising the underlying options package, it is quite interesting,
# in that it requires a mapping of one user-level argument into two
# different underlying parameters. It's a good edge-case for testing.


def test_auto_stringification():
    assert brackets(12) == '[12]'
    assert braces(4.4) == '{4.4}'
    assert double(None) == '"None"'
    assert single(False) == "'False'"


def test_shortcuts():
    assert ' '.join([qs('one'), qd('two'), qt('three'), qb('and'), qdb('four')]) == \
        "'one' \"two\" \"\"\"three\"\"\" `and` ``four``"


def test_instant():
    assert Quoter('+[ ', ' ]+')('castle') == '+[ castle ]+'


def test_lambda():
    f = lambda v: ('(', abs(v), ')') if v < 0 else ('', v, '')
    financial = LambdaQuoter(f)
    assert financial(-10) == '(10)'
    assert financial(44) == '44'

    password = LambdaQuoter(lambda v: ('', 'x' * len(v), ''))
    assert password('secret!') == 'xxxxxxx'

    wf = lambda v:  ('**', v, '**') if v < 0 else ('', v, '')
    warning = lambdaq.warning = LambdaQuoter(wf)
    assert warning(12) == '12'
    assert warning(-99) == '**-99**'
    assert warning(-99, padding=1) == '** -99 **'

    assert lambdaq.warning(12) == '12'
    assert lambdaq.warning(-99) == '**-99**'
    assert lambdaq.warning(-99, padding=1) == '** -99 **'



def test_examples():
    assert single('this') == "'this'"
    assert double('that') == '"that"'
    assert backticks('ls -l') == "`ls -l`"
    assert braces('curlycue') == "{curlycue}"
    assert braces('curlysue', padding=1) == '{ curlysue }'

    bars = Quoter('|')
    assert bars('x') == '|x|'

    plus = Quoter('+', '')
    assert plus('x') == '+x'

    variable = Quoter('${', '}')
    assert variable('x') == '${x}'


def test_attribute_invocations():
    assert single('something') == quote.single('something')
    assert single('something', margin=2, padding=3) == \
           quote.single('something', margin=2, padding=3)
    assert braces('b') == quote.braces('b')

    # now test wholesale
    names = ('braces brackets angles parens qs qd qt qb single double triple '
             'backticks anglequote guillemet chevron curlysingle curlydouble')
    for name in names.split():
        main = eval(name)
        attr = eval('quote.' + name)
        assert main is attr
        assert main('string') == attr('string')


def test_redef():
    braces = Quoter('{', '}', padding=1)
    assert braces('this') == '{ this }'
    assert braces('this', padding=0) == '{this}'
