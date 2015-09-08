
import re
import six
from options import Options, OptionsClass, Prohibited, Transient
from .util import *
from .quoter import Quoter
from .joiner import joinlines
from .styleset import StyleSet


# MD_ATTRS = set(['a', 'p', 'doc', 'h'])
# MD_ATTRS.update(QUOTER_ATTRS)


class MDQuoter(Quoter):

    """
    A more sophisticated quoter for Markdown elements.
    """

    options = Quoter.options.add(
        misc = Prohibited,
    )

    def __init__(self, *args, **kwargs):
        """
        Create an MDQuoter
        """
        # Restating basic init to avoid errors of self.__getattribute__
        # that can flummox superclass instantiation
        super(Quoter, self).__init__()

        opts = self.options = self.__class__.options.push(kwargs)

    def a(self, text, href, **kwargs):
        opts = self.options.push(kwargs)
        parts = ["[", text, "](", href, ")"]
        return self._output(parts, opts)

    def p(self, *args, **kwargs):
        opts = self.options.push(kwargs)
        return self._output(args, opts)

    def doc(self, seq, **kwargs):
        opts = self.options.push(kwargs)
        return joinlines(seq, sep="\n\n")
        # FIXME: kwargs not really used

    def h(self, text, level=1, close=False, setext=False, **kwargs):
        """
        Headers at varous levels. Either atx style (hashmark prefix)
        by default, or Setext (underlining) style optionally.
        """
        opts = self.options.push(kwargs)
        if setext:
            char = '=' if level == 1 else '-'
            parts = [text, '\n', char * len(text), '\n']
        else:
            prefix = "#" * level
            parts = [prefix, ' ', text]
            if close:
                parts.extend([' ', prefix])
        return self._output(parts, opts)

    def h1(self, text, **kwargs):
        kwargs['level'] = 1
        return self.h(text, **kwargs)

    def h2(self, text, **kwargs):
        kwargs['level'] = 2
        return self.h(text, **kwargs)

    def h3(self, text, **kwargs):
        kwargs['level'] = 3
        return self.h(text, **kwargs)

    def h4(self, text, **kwargs):
        kwargs['level'] = 4
        return self.h(text, **kwargs)

    def h5(self, text, **kwargs):
        kwargs['level'] = 5
        return self.h(text, **kwargs)

    def h6(self, text, **kwargs):
        kwargs['level'] = 6
        return self.h(text, **kwargs)

    def h7(self, text, **kwargs):
        kwargs['level'] = 7
        return self.h(text, **kwargs)

    def hr(self, **kwargs):
        opts = self.options.push(kwargs)
        return self._output(['-' * 5], opts)

# see http://daringfireball.net/projects/markdown/syntax
# for basic syntax

# TODO: blockquote
# TODO: code
# TODO: list (ordered)
# TODO: list (unordered)
# TODO: image
# TODO: automatic link
# TODO: footnote
# TODO: table
# TODO: literal asterisks
# TODO: get vsep working

    # need this because basic joiners dont do varargs yet

md = StyleSet(
        factory = MDQuoter,
        immediate = MDQuoter(),
        instant = False,
        promote = 'but clone p a doc h')

md.i = MDQuoter(prefix="*", suffix="*")
md.b = MDQuoter(prefix="**", suffix="**")

# _md_doc = joinlines.but(sep="\n\n")
# MDQuoter.styles['doc'] = _md_doc
# object.__setattr__(MDQuoter, 'doc') == _md_doc

# some obvious glitches and complexities in __getargument__ setup still,
# given complexity of defining doc method - look into
