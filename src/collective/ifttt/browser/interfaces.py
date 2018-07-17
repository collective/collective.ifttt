# -*- coding: utf-8 -*-

from zope.browsermenu.interfaces import IBrowserMenu
from zope.browsermenu.interfaces import IBrowserSubMenuItem
from zope.browsermenu.interfaces import IMenuItemType
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface
from zope.interface import provider


class IContentMenuView(IContentProvider):
    """The view that powers the content menu in the toolbar.

    This will construct a menu by finding an adapter to IContentMenu.
    """

    def available():  # noqa
        """Determine whether the menu should be displayed at all.
        """

    def menu():  # noqa
        """Create a list of dicts that can be used to render a menu.

        The keys in this dict are: title, description, action (a URL),
        selected (a boolean), icon (a URI), extra (a random payload), and
        submenu
        """


# The content menu itself - menu items are registered as adapters to this
# interface (this is signalled by marking the interface itself with the
# IInterface IMenuItemType)


@provider(IMenuItemType)
class IContentMenuItem(Interface):
    """Special menu item type for Plone's content menu."""


class IftttTriggerSubMenuItem(IBrowserSubMenuItem):
    """The menu item linking to the actions menu.
    """


class IftttTriggersMenu(IBrowserMenu):
    """The actions menu.

    This gets its menu items from portal_actions.
    """
