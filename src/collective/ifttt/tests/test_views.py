# -*- coding: utf-8 -*-
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from plone import api
from plone.contentrules.engine.interfaces import IRuleStorage
from zope.component import getMultiAdapter
from zope.component import queryUtility

import unittest


class TestRules(unittest.TestCase):

    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):
        """utility setup for tests"""

        self.context = self.layer['portal']
        self.request = self.layer['request']
        self.views = getMultiAdapter((self.context, self.request),
                                     name='checkifttt')

    def test_ifttt(self):

        self.assertEqual(False, self.views.check_iftttconfig())

        api.portal.set_registry_record(
            name='ifttt.ifttt_secret_key',
            value=u'secret',
        )
        self.assertEqual(True, self.views.check_iftttconfig())

        storage = queryUtility(IRuleStorage)
        storage.active = False
        self.assertEqual(False, self.views.check_iftttconfig())
