"""Data manipulation functions

"""

import decimal
import babel.numbers
import locale

## XXXvlab: we can't import any module without having to
## import all openerp. That's sad. I can't do easy tests of
## my code.
from openerp.addons.report_xml.mako_tools import \
     MakoParsable, unwrap, mako_env


from .register import register


@register
def group_by(elts, key):
    heaps = {}
    for elt in elts:
        k = key(elt)
        heaps[k] = heaps.get(k, []) + [elt]
    return heaps


@register
def format_decimal(amount, lang=None, format='#,##0.00', **kwargs):
    """Format any amount in the given format and locale

    >>> format_decimal('2813.7456', lang='en')
    '2,813.74'

    >>> format_decimal('2813.7456', lang='fr')
    '2 813,74'

    >>> format_decimal('2813.7456', lang='fr', format='#,###0.000')
    '2813,746'

    """
    if lang is None:
        lang = mako_env().get("lang", None)
    amount = unwrap(amount)
    return babel.numbers.format_decimal(
        decimal.Decimal(amount), format=format,
        locale=lang, **kwargs)


@register
def escape_xml(str):
    return str.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


@register
def locale_format(fmt, value):
    return locale.format(fmt, unwrap(value))
