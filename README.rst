zendeskpy
=========

python module for interacting with the zendesk help center api

Example Code
~~~~~~~~~~~~

Here's a simple example for using the module.

.. code::

    from zendeskhc.HelpCenter import HelpCenter

    hc = HelpCenter("https://mysubdomain.zendesk.com")
    categories = hc.list_all_categories()
    sections = hc.list_all_sections()
