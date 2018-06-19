# -*- coding: utf-8 -*-
from plone import api
from Products.Five.browser import BrowserView


class checkView(BrowserView):
    def check_iftttconfig(self):

        # check if IFTTT secret key is added
        secret_key = api.portal.get_registry_record('ifttt.ifttt_secret_key')
        if not secret_key:
            return False
        return True
