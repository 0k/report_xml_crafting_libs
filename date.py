"""Function to ease writing of mako templates

Note that you can run the doctest with:

    python -m doctest date.py

"""


try:
    from openerp.addons.report_xml.mako_tools import \
         MakoParsable, unwrap
except ImportError:  ## for tests
    class MakoParsable(object):
        def __init__(self, obj):
            self._obj = obj
        def __repr__(self):
            return repr(self._obj)

    def wrap(elt):
        return MakoParsable(elt) if not isinstance(elt, MakoParsable) else elt

    def unwrap(elt):
        return getattr(elt, "_obj") if isinstance(elt, MakoParsable) else elt


from babel import dates
from datetime import datetime, date
from sact.epoch import Time, UTC, TzLocal

import time

try:
    from .register import register
except ValueError: ## for tests
    def register(f):
        return f


@register
def format_date(mp, locale, format="long", hours=False):
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

    And you can ask for displaying hours also::

        >>> format_date(epoch_string, "en", format="medium", hours=True)
        u'Oct 10, 2000, 12:00:00 AM'

    """
    raw = unwrap(mp)
    if isinstance(raw, basestring):
        dt = Time(raw, hint_src_tz=UTC())
    elif isinstance(raw, datetime) or isinstance(raw, date):
        dt = Time(raw, hint_src_tz=UTC())
    else:
        return MakoParsable(None)
    fun = dates.format_datetime if hours else dates.format_date
    return MakoParsable(
        fun(dt, format=format, locale=locale))


@register
def strftime(mp, fmt):
    """Format a MakoParsable date as a date in time.strftime provided format

    Usage
    =====

    Let's create two MakoParsable date:

        >>> epoch_datetime = MakoParsable(datetime.utcfromtimestamp(0))
        >>> epoch_string = MakoParsable("2000-10-10")

    ``format_date`` should convert to the accurate human local representation
    of these date:

        >>> strftime(epoch_datetime, "%Y")
        u'1970'
        >>> strftime(epoch_string, "%Y-%m")
        u'2000-10'

    Acceptance of both format is required for conveniency as OOOP object and
    OpenERP object do not behave the same way when accessing datetime objects.

    Please note that providing a non-string / date object will result by
    returning a MakoParsable(None):

        >>> format_date(MakoParsable(2), "fr")
        None
        >>> type(format_date(MakoParsable(2), "fr"))  # doctest: +ELLIPSIS
        <class '...MakoParsable'>


    """
    raw = unwrap(mp)
    if not raw:
        return MakoParsable(None)
    return MakoParsable(Time(raw, hint_src_tz=UTC()).strftime(fmt))
