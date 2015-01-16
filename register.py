# -*- coding: utf-8 -*-


ENV = {}


try:
    import openerp.addons.report_xml.mako_tools as mako_tools
except ImportError:
    mako_tools = None


try:
    import openerp.addons.base.ir.ir_ui_view as ir_ui_view
except ImportError:
    ir_ui_view = None


def register(f):
    """Decorator helper to register function in different environement"""

    ENV[f.__name__] = f
    if mako_tools:
        mako_tools.env[f.__name__] = f
    if ir_ui_view and hasattr(ir_ui_view, "QWEB_DEFAULT_CONTEXT"):
        ir_ui_view.QWEB_DEFAULT_CONTEXT[f.__name__] = f
    return f
