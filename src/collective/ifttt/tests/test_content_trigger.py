# -*- coding: utf-8 -*-
from collective.ifttt.actions.ifttt import PAYLOAD_DESCRIPTION
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from plone.app.contentrules.conditions.wfstate import WorkflowStateCondition
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from Products.CMFCore.interfaces._events import IActionSucceededEvent
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class TestActionMenu(unittest.TestCase):
    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']

    def test_view(self):
        # Check existence of IFTTT Action Menu

        self.view = getMultiAdapter((self.portal, self.request),
                                    name='ifttt_content_trigger')
        actions_view = self.view()
        self.assertIn('including the description of content', actions_view)

    def test_add(self):

        self.request.method = 'POST'
        self.request.form['form.widgets.ifttt_event_name'] = 'Test'
        self.request.form['form.widgets.content_types'] = [
            'Document', 'News Item'
        ]
        self.request.form['form.widgets.workflow_transitions'] = [
            'publish', 'reject'
        ]
        self.request.form['form.buttons.add'] = u'Add'
        self.view = getMultiAdapter((self.portal, self.request),
                                    name='ifttt_content_trigger')
        self.view()

        storage = getUtility(IRuleStorage)

        # check that rule has been successfully created
        self.assertEqual(1, len(storage.values()))
        self.assertEqual(IActionSucceededEvent, storage.values()[0].event)
        # workflow_state to be published is
        # default condition of content_trigger
        self.assertEqual(5, len(storage.values()[0].conditions))
        self.assertEqual(
            WorkflowStateCondition,
            storage.values()[0].conditions[-1].__class__
        )
        self.assertEqual(
            'Test',
            storage.values()[0].actions[0].ifttt_event_name
        )
        self.assertEqual(
            'plone.actions.Ifttt',
            storage.values()[0].actions[0].element
        )
        self.assertEqual(
            PAYLOAD_DESCRIPTION,
            storage.values()[0].actions[0].payload_option
        )
