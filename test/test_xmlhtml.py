from quoter import *
import pytest


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


# some problem exists with explicit atts setting here
@pytest.mark.skipif('True')
def test_xml_autogenerate():
    more = xml.b.clone(atts='.this')
    assert more('x') == "<b class='this'>x</b>"
