# -*- coding: utf-8 -*-
from collective.ifttt import _
from collective.ifttt.browser.interfaces import IftttTriggersMenu
from collective.ifttt.browser.interfaces import IftttTriggerSubMenuItem
from plone.app.contentmenu.menu import ActionsSubMenuItem
from plone.memoize.instance import memoize
from plone.protect.utils import addTokenToUrl
from zope.browsermenu.menu import BrowserMenu
from zope.component import getMultiAdapter
from zope.interface import implementer

import plone.api as api


@implementer(IftttTriggerSubMenuItem)
class IftttTriggersSubMenuItem(ActionsSubMenuItem):
    title = _(
        u'label_ifttt_menu',
        default=u'IFTTT',
    )
    description = _(
        u'title_ifttt_menu',
        default=u'IFTTT trigger content rules for the current content item',
    )
    submenuId = 'plone_contentmenu_ifttttriggers'
    order = 35
    extra = {
        'id': 'plone-contentmenu-ifttttriggers',
        'li_class': 'plonetoolbar-content-action'
    }

    @memoize
    def available(self):
        actions_tool = api.portal.get_tool('portal_actions')
        actions = actions_tool.listActionInfos(
            object=self.context, categories=('object_ifttt_triggers', ), max=1
        )
        return len(actions) > 0


@implementer(IftttTriggersMenu)
class IftttTriggersMenu(BrowserMenu):
    def getMenuItems(self, context, request):
        """Return menu item entries in a TAL-friendly form."""
        results = []

        context_state = getMultiAdapter((context, request),
                                        name='plone_context_state')
        context_state = getMultiAdapter(
            (context_state.canonical_object(), request),
            name='plone_context_state'
        )
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
                css_class += ' pat-plone-modal'

            results.append({
                'title': action['title'],
                'description': '',
                'action': addTokenToUrl(action['url'], request),
                'selected': False,
                'icon': icon,
                'extra': {
                    'id': 'plone-contentmenu-ifttttriggers-' + aid,
                    'separator': None,
                    'class': css_class,
                    'modal': modal,
                },
                'submenu': None,
            })
        return results
