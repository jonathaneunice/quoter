

 *  set up styleset so one can make a namespaced XMLQuoter like inv

 *  document multiple arg Quoter and broader pair interpreation

 *  improve pair interpretation to work with magic arguments not bespoke logic

 *  add fork interprestation once nomenclature dust settles

 *  flesh out Markdown formatter with code, list, listitem, etc

 *  use MD to add indent kind of functions (block oriented layout)

    The problem with this is that we're returning strings all the time,
    and yet also trying to generate relatively structured output. For
    inline span type of quoting, this is fine. For multi-level indented
    structures, less so. Consider `div(div(div('text')))`. Ideally that
    would render indented text. Something like:

        <div>
            <div>
                <div>text</div>
            <div>
        </div>

    But the problem is that the innermost `div()` will be evaluated first,
    and it has no idea how indented it will ultimately be.
    If quoters could return a object that stringifies
    or renders to string, but is not itself a string, things would be
    easier.  We could create a more-or-less parse tree, which when
    stringified/rendered would interpret all the different levels. That's
    a fine design decision for a markup-rendering library, but fits less
    well with our string-quoting design.

    As a workaround, we're going to set some rules on what constitutes a
    "block" element, and how they are rendered. Then we'll use those rules
    to determine if inner items need to be indented by outer items. To wit,
    block elements will end with a newline (`'\n'`). `div('text`)` e.g. will
    return `'<div>text</div>\n'`.  This way, a simple test
    (`o.endsith('\n')`) will let us determine if a string is to be considered
    block text. This will allow us to build nice indentation in.

    There are tradeoffs. Text wrapping is one. Ideally a text-oriented block
    element like `<p>` would have its enclosed text wrapped to a reasonable
    line width. Except, if the paragraph is within a few divs, and maybe a
    body and html, those outer elements will add their own indentation after
    the paragraph is rendered. The nice wrap-to-80-columns logic goes out
    the window, because the lines are now 100 characters wide. The global
    structure is not available at the time the formatting is done. This can
    be someone ameliorated by having the block elements which tend to have
    significant text content (p, blockquote, and li, e.g.) set modest wrap
    widths. If they set 60 say, there is a lot of extra room for
    indentation. While imperfect, it could go a long way to being
    a Pareto-sufficient solution.

    This is now prototyped, but there is a considerable issue with <pre>
    which is going to get indented even if it's wrong to do so, because
    of the mulitple levels after the pre that will indent not knowing about
    the pre. Maybe a fix_pre routine would do - strip out all the common
    prefix of pre sections.

 *  determine if problem with multinamed styles in quoter (seems like it)
 *  further modulularize documentation
 *  Add support for alternate XML types such as declarations and
    processing instructions,
    CDATA and PCDATA sections, etc. (CDATA, PCDATA, and comments at least
    partially done already)
 *  consider different exports for the different module levels

 *  Eventually working way toward a CSS box model style formatting in which there
    can be a marginleft, marginright, paddingleft, and paddingright (i.e.
    separating left and right magin/padding specs). It might even be possible
    to provide borders (top and bottom), and to reconsider prefix and suffix
    as left and right borders. Alignment of content within a cell and various
    forms of multi-line justification might also be feasible.

 *  add htmlenttity aliases to base quoter

    On second thought, how would this work? Most of the quotation
    systems involve paired glyphs. If a quoter were called quote.lsquo,
    would that imply a &rsquo; right-side pariing? As the [Wikipedia page
    on quotation marks](https://en.wikipedia.org/wiki/Quotation_mark)
    shows, sometimes those pairings aren't symmetric. Tabling this idea
    for now as a probable "sounds better initially than it will really
    work out in practice" item.
