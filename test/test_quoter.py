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


def test_clone():
    # make sure clones properly registered just like normally defined
    # styles, that clones are different from original, that they yield
    # the expected results, and that after cloning, the originals
    # behave exactly as before

    bar2 = brackets.clone(margin=2, name='bar2')
    assert bar2 is not brackets
    assert bar2('this') == '  [this]  '
    assert brackets('this') == '[this]'
    assert quote.bar2('this') == '  [this]  '

    bb = html.b.clone(padding=1, margin=2)
    assert bb is not html.b
    assert 'bb' not in HTMLQuoter.styles
    assert bb('this') == '  <b> this </b>  '
    assert html.b('this') == '<b>this</b>'


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
    bar2 = brackets.clone(margin=2, name='bar2')
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


# NB There is an error in namespace managment.
# HTML attributes should be limited to HTMLQuoter,
# but there is currently leakage. Styles seem to be
# defined in Quoter, not the most proximate superclass


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
    warning = LambdaQuoter(wf, name='warning')
    assert warning(12) == '12'
    assert warning(-99) == '**-99**'
    assert warning(-99, padding=1) == '** -99 **'

    assert lambdaq.warning(12) == '12'
    assert lambdaq.warning(-99) == '**-99**'
    assert lambdaq.warning(-99, padding=1) == '** -99 **'


def test_lambdaq_named_style():
    assert lambdaq(44, style='warning') == '44'
    assert lambdaq(-44, style='warning') == '**-44**'


def test_html_examples():
    assert html.p("A para", ".focus") == "<p class='focus'>A para</p>"
    assert html.img('.large', src='file.jpg') in [
        "<img class='large' src='file.jpg'>",
        "<img src='file.jpg' class='large'>"
        ]
    assert html.br() == "<br>"
    assert html.comment("content ends here") == "<!-- content ends here -->"


    assert html('hey', 'p#one.main.special[lang=en]') in [
        "<p id='one' class='main special' lang='en'>hey</p>",
        "<p id='one' lang='en' class='main special'>hey</p>",
        "<p class='main special' id='one' lang='en'>hey</p>",
        "<p class='main special' lang='en' id='one'>hey</p>",
        "<p lang='en' id='one' class='main special'>hey</p>",
        "<p lang='en' class='main special' id='one'>hey</p>",
        ]
        # all the permutations!


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

    variable = Quoter('${', '}', name='variable')
    assert variable('x') == '${x}'


def test_attribute_invocations():
    assert single('something') == quote.single('something')
    assert single('something', margin=2, padding=3) == quote.single('something', margin=2, padding=3)
    assert braces('b') == quote.braces('b')

    # now test wholesale
    names = 'braces brackets angles parens qs qd qt qb single double triple ' +\
            'backticks anglequote guillemet curlysingle curlydouble'
    for name in names.split():
        main = eval(name)
        attr = eval('quote.' + name)
        assert main is attr
        assert main('string') == attr('string')


def test_quote_shortcut():
    variable = Quoter('${', '}', name='variable')
    assert variable('x') == '${x}'

    assert quote('myvar', style='variable') == '${myvar}'

    assert quote('this', style='braces') == '{this}'


def test_named_quote_style():
    assert quote('this', style='variable') == '${this}'
    assert braces('this', style='variable') == '${this}'


def test_redef():
    braces = Quoter('{', '}', padding=1, name='braces')
    assert braces('this') == '{ this }'
    assert braces('this', padding=0) == '{this}'


def test_para():
    para = HTMLQuoter('p')
    # assert para('this is great!', {'class':'emphatic'}) == "<p class='emphatic'>this is great!</p>"
    assert para('this is great!', '.emphatic') == "<p class='emphatic'>this is great!</p>"
    assert para('First para!', '#first') == "<p id='first'>First para!</p>"
    assert para('First para!', '#first', atts='.one') in [
        "<p id='first' class='one'>First para!</p>",
        "<p class='one' id='first'>First para!</p>"]

    para_e = HTMLQuoter('p.emphatic')
    assert para_e('this is great!') == "<p class='emphatic'>this is great!</p>"
    assert para_e('this is great?', '.question') == "<p class='question emphatic'>this is great?</p>"

    para = HTMLQuoter('p', attquote=double)
    assert para('this is great!', {'class':'emphatic'}) == '<p class="emphatic">this is great!</p>'

    div = HTMLQuoter('div', attquote=double)
    assert div('something', '.todo') == '<div class="todo">something</div>'


def test_css_selector():
    assert html('joe', 'b.name') == "<b class='name'>joe</b>"
    assert xml('joe', 'b.name') == "<b class='name'>joe</b>"

    assert xml('joe', 'name#emp0193') == "<name id='emp0193'>joe</name>"


def test_void():
    br = HTMLQuoter('br', void=True)
    assert br() == '<br>'

    img = HTMLQuoter('img', void=True)
    assert img() == '<img>'
    assert img(src="this") == "<img src='this'>"
    assert img('.roger', src="this") == "<img class='roger' src='this'>" or \
           img('.roger', src="this") == "<img src='this' class='roger'>"


def test_xml_examples():
    item = XMLQuoter(tag='item', ns='inv', name='item inv_item')
    assert item('an item') == '<inv:item>an item</inv:item>'
    assert xml.item('another') == '<inv:item>another</inv:item>'
    assert xml.inv_item('yet another') == '<inv:item>yet another</inv:item>'
    assert xml.thing('something') == '<thing>something</thing>'
    assert xml.special('else entirely', '#unique') == \
            "<special id='unique'>else entirely</special>"


def test_xml_auto_and_attributes():

    assert xml.root('this') == '<root>this</root>'
    assert xml.root('this', ns='one') == '<one:root>this</one:root>'
    assert xml.branch('that') == '<branch>that</branch>'
    assert xml.branch('that', ns='two') == '<two:branch>that</two:branch>'

    assert xml.comment('hidden') == '<!-- hidden -->'
    assert xml.comment('hidden', padding=0) == '<!--hidden-->'


def test_html_auto_and_attributes():
    assert html.b('bold') == '<b>bold</b>'
    assert html.emphasis('bold') == '<emphasis>bold</emphasis>'
    assert html.strong('bold') == '<strong>bold</strong>'
    assert html.strong('bold', padding=1) == '<strong> bold </strong>'
    assert html.strong('bold', margin=1) == ' <strong>bold</strong> '

    assert html.comment('XYZ') == '<!-- XYZ -->'
    assert html.comment('XYZ', padding=0) == '<!--XYZ-->'

    assert html.br() == '<br>'
    assert html.img(src='one') == "<img src='one'>"


def test_named_styles_in_proper_homes():
    assert 'x' not in Quoter.styles
    assert 'x' not in HTMLQuoter.styles
    assert 'x' not in XMLQuoter.styles

    x = Quoter('X', name='x')
    assert x('y') == 'XyX'
    assert 'x' in Quoter.styles

    assert html.x("y") == "<x>y</x>"
    assert 'x' in HTMLQuoter.styles

    assert xml.x("y") == "<x>y</x>"
    assert 'x' in XMLQuoter.styles


def test_named_xml_and_html_styles():
    XMLQuoter('book', name='book')
    assert xml("this", style="book") == "<book>this</book>"


def test_bad_style_names():
    with pytest.raises(BadStyleName):
        v = Quoter('v', name="_v")


# some problem exists with explicit atts setting here
@pytest.mark.skipif('True')
def test_xml_autogenerate():
    more = xml.b.clone(atts='.this')
    assert more('x') == "<b class='this'>x</b>"
