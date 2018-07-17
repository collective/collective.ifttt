# -*- coding: utf-8 -*-

from collective.ifttt import _
from collective.ifttt.browser.interfaces import IftttTriggersMenu
from collective.ifttt.browser.interfaces import IftttTriggerSubMenuItem
from plone.api.portal import get_tool
from plone.memoize.instance import memoize
from plone.protect.utils import addTokenToUrl
# from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from zope.browsermenu.menu import BrowserMenu
from zope.browsermenu.menu import BrowserSubMenuItem
from zope.component import getMultiAdapter
from zope.interface import implementer


@implementer(IftttTriggerSubMenuItem)
class IftttTriggerSubMenuItem(BrowserSubMenuItem):

    title = _(u'label_actions_menu', default=u'Actions')
    description = _(
        u'title_actions_menu', default=u'Actions for the current content item'
    )
    submenuId = 'plone_contentmenu_iftttactions'

    order = 30
    extra = {
        'id': 'plone-contentmenu-actions',
        'li_class': 'plonetoolbar-content-action'
    }

    def __init__(self, context, request):
        super(IftttTriggerSubMenuItem, self).__init__(context, request)
        self.context_state = getMultiAdapter((context, request),
                                             name='plone_context_state')

    @property
    def action(self):
        folder = self.context
        if not self.context_state.is_structural_folder():
            folder = utils.parent(self.context)
        return folder.absolute_url() + '/folder_contents'

    @memoize
    def available(self):
        actions_tool = api.portal.get_tool('portal_actions')
        actions = actions_tool.listActionInfos(
            object=self.context, categories=('object_ifttt_triggers', ), max=1
        )
        return len(editActions) > 0

    def selected(self):
        return False


@implementer(IftttTriggersMenu)
class IftttTriggersMenu(BrowserMenu):
    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        context_state = getMultiAdapter((context, request),
                                        name='plone_context_state')
        actions = context_state.actions('object_ifttt_triggers')
        if not actions:
            return results

        for action in actions:
            if not action['allowed']:
                continue
            aid = action['id']
            css_class = 'actionicon-object_ifttt_triggers-{0}'.format(aid)
            icon = action.get('icon', None)
            modal = action.get('modal', None)
            if modal:
                cssClass += ' pat-plone-modal'

            results.append({
                'title': action['title'],
                'description': '',
                'action': addTokenToUrl(action['url'], request),
                'selected': False,
                'icon': icon,
                'extra': {
                    'id': 'plone-contentmenu-actions-' + aid,
                    'separator': None,
                    'class': cssClass,
                    'modal': modal
                },
                'submenu': None,
            })
        return results
