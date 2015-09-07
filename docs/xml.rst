XML
===

``XMLQuoter`` with its ``xml`` front-end is a similar quoter with markup
intelligence. It offers
one additional attribute beyond ``HTMLQuoter``:
``ns`` for namespaces. Thus::

    item = xml._define("item inv_item", tag='item', ns='inv')
    print item('an item')
    print xml.item('another')
    print xml.inv_item('yet another')
    print xml.thing('something')
    print xml.special('else entirely', '#unique')

yields::

    <inv:item>an item</inv:item>
    <inv:item>another</inv:item>
    <inv:item>yet another</inv:item>
    <thing>something</thing>
    <special id='unique'>else entirely</special>

Note: ``item`` was given two names. Multiple aliases are supported.
While the ``item`` object carries its namespace specification through its
different invocations, the calls to non-``item`` quoters nave no persistent
namespace. Finally, that the CSS specification language heavily used in
HTML is present and available for XML, though its use may be less common.

In general, ``xml.tagname`` auto-generates quoters just like
``html.tagname`` does on first use. There are also pre-defined utility
methods such as ``html.comment()`` and ``xml.comment()`` for commenting
purposes.
