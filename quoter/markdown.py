
import re
import six
from options import Options, OptionsClass, Prohibited, Transient
from .util import *
from .quoter import Quoter, QUOTER_ATTRS
from .joiner import joinlines

# from show import *
def show(*args, **kwargs):
    pass


MD_ATTRS = set(['a', 'p', 'doc'])
MD_ATTRS.update(QUOTER_ATTRS)

class MDQuoter(Quoter):

    """
    A more sophisticated quoter for Markdown elements.
    """

    styles = {}         # remember named styles

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
        self._register_name(opts.name)

    def __getattribute__(self, name):
        if name in MD_ATTRS or name.startswith('_'):
            return object.__getattribute__(self, name)
        cls = object.__getattribute__(self, '__class__')
        cdict = object.__getattribute__(cls, '__dict__')
        if name in cdict:
            return cdict[name]
        return cls(name, name=name)

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

    # need this because basic joiners dont do varargs yet

md = MDQuoter()

md.i = MDQuoter(prefix="*", suffix="*", name='i')
md.b = MDQuoter(prefix="**", suffix="**", name='b')

# _md_doc = joinlines.but(sep="\n\n")
# MDQuoter.styles['doc'] = _md_doc
# object.__setattr__(MDQuoter, 'doc') == _md_doc

# some obvious glitches and complexities in __getargument__ setup still,
# given complexity of defining doc method - look into
