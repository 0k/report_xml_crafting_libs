"""Data manipulation functions

"""


from openerp.addons.report_xml.mako_tools import register, MakoParsable


@register
def group_by(elts, key):
    heaps = {}
    for elt in elts:
        k = key(elt)
        heaps[k] = heaps.get(k, []) + [elt]
    return heaps
