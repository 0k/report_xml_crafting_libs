OpenERP module that provides some convienient shortcuts for crafting XML Mako reports

Requirements
============

This module depends on ``report_xml`` module and will work on OpenERP v6.1 and v7.0


Functions
=========


format_date
-----------

You can use format_date to display a full date in the correct internationalized manner.

For instance::

    ...
    ${format_date(object.date_start, "en")}
    ...

Will output::

    ...
    October 10, 2000
    ...

For more info, check the docstring of ``format_date()`` in the code.


group_by
--------

This methods allow to group a list depending on the output of a function. This could
allow you to group ``sale_order_lines`` depending on attribute ``product_id.category``
for instance::

    ...
    <%
    categs = group_by(object.abstract_line_ids,
                      key=lambda al: al.product_id.categ_id.complete_name)
    %>
    % for categ, lines in categs.iteritems(): 
        <category name="${categ.name}">

        % for line in lines:
            <line>
                <product>${line.product_id.default_code}</product>
                ...
            </line>
        %endfor
        </category>
    % endfor
    ...


