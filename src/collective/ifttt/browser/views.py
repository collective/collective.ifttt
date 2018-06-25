# -*- coding: utf-8 -*-
from plone import api
from plone.contentrules.engine.interfaces import IRuleAssignable
from plone.contentrules.engine.interfaces import IRuleStorage
from Products.Five.browser import BrowserView
from zope.component import queryUtility


class checkView(BrowserView):
    def check_iftttconfig(self):

        # check that we are on a folder where content rules can be assigned
        if not IRuleAssignable.providedBy(self.context):
            return False

        # checks that content rules are not globally disabled
        # from content rules control panel
        storage = queryUtility(IRuleStorage)
        if not storage.active:
            return False

        # check if IFTTT secret key is added
        secret_key = api.portal.get_registry_record('ifttt.ifttt_secret_key')
        if not secret_key:
            return False
        return True
