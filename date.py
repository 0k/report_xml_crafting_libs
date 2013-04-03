"""Questionnable wrapping object and function to ease writing of mako templates

Note that you can run the doctest with:

    python -m doctest date.py

"""


from openerp.addons.report_xml.mako_tools import register, MakoParsable


from babel.dates import format_date as babel_format_date
from datetime import datetime, date
import time


@register
def format_date(mp, locale):
    """Format a MakoParsable object as a date in provided locale

    Usage
    =====

    Let's create two MakoParsable date:

        >>> epoch_datetime = MakoParsable(datetime.utcfromtimestamp(0))
        >>> epoch_string = MakoParsable("2000-10-10")

    ``format_date`` should convert to the accurate human local representation
    of these date:

        >>> format_date(epoch_datetime, "fr")
        u'1 janvier 1970'
        >>> format_date(epoch_string, "fr")
        u'10 octobre 2000'

    Acceptance of both format is required for conveniency as OOOP object and
    OpenERP object do not behave the same way when accessing datetime objects.

    Please note that providing a non-string / date object will result by
    returning a MakoParsable(None):

        >>> format_date(MakoParsable(2), "fr")
        None
        >>> type(format_date(MakoParsable(2), "fr"))  # doctest: +ELLIPSIS
        <class '...MakoParsable'>

    Please note that other languages are supported:

        >>> format_date(epoch_string, "en")
        u'October 10, 2000'
        >>> format_date(epoch_string, "de")
        u'10. Oktober 2000'

    """
    if not isinstance(mp, MakoParsable):
        raise TypeError("Argument %r is not a MakoParsable." % mp)

    raw = getattr(mp, "_obj")

    if isinstance(raw, basestring):
        dt = datetime.strptime(raw, "%Y-%m-%d")
    elif isinstance(raw, datetime) or isinstance(raw, date):
        dt = raw
    else:
        return MakoParsable(None)
    return MakoParsable(babel_format_date(dt,
                                          format="long",
                                          locale=locale))


# @register
# def strftime(mp, fmt):
#     """Format a MakoParsable date as a date in time.strftime provided format

#     Usage
#     =====

#     Let's create two MakoParsable date:

#         >>> epoch_datetime = MakoParsable(datetime.utcfromtimestamp(0))
#         >>> epoch_string = MakoParsable("2000-10-10")

#     ``format_date`` should convert to the accurate human local representation
#     of these date:

#         >>> strftime(epoch_datetime, "%Y")
#         u'1970'
#         >>> strftime(epoch_string, "%Y-%m")
#         u'2000-10'

#     Acceptance of both format is required for conveniency as OOOP object and
#     OpenERP object do not behave the same way when accessing datetime objects.

#     Please note that providing a non-string / date object will result by
#     returning a MakoParsable(None):

#         >>> format_date(MakoParsable(2), "fr")
#         None
#         >>> type(format_date(MakoParsable(2), "fr"))  # doctest: +ELLIPSIS
#         <class '...MakoParsable'>


#     """
#     if not isinstance(mp, MakoParsable):
#         raise TypeError("Argument %r is not a MakoParsable.")

#     raw = getattr(mp, "_obj")

#     if not raw:
#         return MakoParsable(None)
#     return MakoParsable(time.strftime(raw, fmt))

