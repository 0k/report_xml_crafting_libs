# -*- coding: utf-8 -*-
"""function to ease writing of mako templates

Note that you can run the doctest with:

    python -m doctest date.py

"""


from openerp.addons.report_xml.mako_tools import mako_env, \
     MakoParsable

from .register import register


@register
def search(model, domain, context=None):
    env = mako_env()
    if context is None:
        context = env["_context"]
    context = context.copy()
    m = env["_pool"].get(model)
    ids = m.search(env["_cr"], env["_uid"], domain, context=context)
    return [MakoParsable(r)
            for r in m.browse(env["_cr"], env["_uid"], ids,
                              context=env["_context"])]


@register
def search_one(model, domain, context=None):
    s = search(model, domain, context)
    if len(s) != 1:
        raise Exception("Search_one on model %s and domain %r gave %d object."
                        % (model, domain, len(s)))
    return s[0]
