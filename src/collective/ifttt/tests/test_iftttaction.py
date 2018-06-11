# -*- coding: utf-8 -*-
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.rule.interfaces import IRuleAction
from zope.component import getUtility

import unittest


class IftttTests(unittest.TestCase):

    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']

    def test_action_registered(self):
        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        self.assertEqual('plone.actions.Ifttt', element.addview)
        self.assertEqual('edit', element.editview)
        self.assertEqual('Ifttt Trigger Action', element.title)
