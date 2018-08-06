# -*- coding: utf-8 -*-

from collective.ifttt import _
from collective.ifttt.actions.ifttt import PAYLOAD_DESCRIPTION
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from collective.ifttt.utils import Rules
from plone.app.contentrules.conditions.portaltype import PortalTypeCondition
from plone.app.contentrules.conditions.wfstate import WorkflowStateCondition
from plone.app.contentrules.conditions.wftransition import WorkflowTransitionCondition  # noqa: E501
from plone.contentrules.engine.interfaces import IRuleAssignmentManager
from plone.contentrules.engine.interfaces import IRuleStorage
from Products.CMFCore.interfaces._events import IActionSucceededEvent
from zope.component import getUtility

import unittest


class TestRules(unittest.TestCase):

    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):
        """utility setup for tests"""

        self.context = self.layer['portal']
        self.request = self.layer['request']
        self.rules = Rules(self.context, self.request)

    def get_testData(self):
        test_data = {
            'ifttt_event_name': 'Test',
            'content_types': ('Folder', 'Discussion Item', 'News Item'),
            'workflow_transitions': ('publish', 'reject'),
            'workflow_states': ('published', ),
            'payload': PAYLOAD_DESCRIPTION,
            'event': IActionSucceededEvent,
        }
        return test_data

    def test_add(self):

        self.rules.add_rule(self.get_testData())
        storage = getUtility(IRuleStorage)
        self.assertEqual(1, len(storage.values()))
        self.assertEqual(
            _(u'${title}_Trigger_${ifttt_event_name}'),
            storage.values()[0].title
        )
        self.assertEqual(True, storage.values()[0].enabled)
        self.assertEqual(False, storage.values()[0].stop)
        self.assertEqual(False, storage.values()[0].cascading)
        self.assertEqual(IActionSucceededEvent, storage.values()[0].event)

    def test_configuration(self):

        self.rules.add_rule(self.get_testData())
        self.rules.configure_rule(self.get_testData())
        storage = getUtility(IRuleStorage)
        self.assertEqual(6, len(storage.values()[0].conditions))
        self.assertEqual(
            PortalTypeCondition,
            storage.values()[0].conditions[0].__class__
        )
        self.assertEqual(
            WorkflowTransitionCondition,
            storage.values()[0].conditions[3].__class__
        )
        self.assertEqual(
            WorkflowStateCondition,
            storage.values()[0].conditions[5].__class__
        )
        self.assertEqual(
            'plone.actions.Ifttt',
            storage.values()[0].actions[0].element
        )
        self.assertEqual(
            'Test',
            storage.values()[0].actions[0].ifttt_event_name
        )
        self.assertEqual(
            PAYLOAD_DESCRIPTION,
            storage.values()[0].actions[0].payload_option
        )

    def test_assigning(self):

        self.rules.add_rule(self.get_testData())
        self.rules.configure_rule(self.get_testData())
        self.rules.apply_rule()
        rule = IRuleAssignmentManager(self.context)
        self.assertTrue('rule-1' in rule)
        self.assertTrue(rule['rule-1'].enabled)
        self.assertTrue(rule['rule-1'].bubbles)
