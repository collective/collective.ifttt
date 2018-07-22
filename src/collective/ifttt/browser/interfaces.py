# -*- coding: utf-8 -*-
from zope.browsermenu.interfaces import IBrowserMenu
from zope.browsermenu.interfaces import IBrowserSubMenuItem


class IftttTriggerSubMenuItem(IBrowserSubMenuItem):
    """The menu item linking to the actions menu.
    """


class IftttTriggersMenu(IBrowserMenu):
    """The actions menu.

    This gets its menu items from portal_actions.
    """
