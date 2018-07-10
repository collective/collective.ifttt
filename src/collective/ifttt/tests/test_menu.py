# -*- coding: utf-8 -*-
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter

import unittest


class TestActionMenu(unittest.TestCase):
    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.view = getMultiAdapter(
            (self.layer['portal'], self.layer['request']),
            name='ifttt_content_trigger'
        )

    def test_view(self):
        # Check existence of IFTTT Action Menu

        actions_view = self.view()
        self.assertIn('This will add new IFTTT Trigger', actions_view)
