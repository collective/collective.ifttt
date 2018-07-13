# -*- coding: utf-8 -*-
from collective.ifttt.actions.ifttt import PAYLOAD_USERNAME
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from plone.app.contentrules.conditions.wfstate import WorkflowStateCondition  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

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
                                    name='ifttt_user_trigger')
        actions_view = self.view()
        self.assertIn(
            'including the information of who changed it', actions_view
        )

    def test_add(self):

        self.request.method = 'POST'
        self.request.form['form.widgets.ifttt_event_name'] = 'Test'
        self.request.form['form.widgets.content_types'] = [
            'Document', 'News Item'
        ]
        self.request.form['form.buttons.add'] = u'Add'
        self.view = getMultiAdapter((self.portal, self.request),
                                    name='ifttt_user_trigger')
        self.view()

        storage = getUtility(IRuleStorage)

        # check that rule has been successfully created
        self.assertEqual(1, len(storage))
        self.assertEqual(IObjectModifiedEvent, storage.values()[0].event)
        self.assertEqual(2, len(storage.values()[0].conditions))
        self.assertEqual(
            'Test',
            storage.values()[0].actions[0].ifttt_event_name
        )
        self.assertEqual(
            'plone.actions.Ifttt',
            storage.values()[0].actions[0].element
        )
        self.assertEqual(
            PAYLOAD_USERNAME,
            storage.values()[0].actions[0].payload_option
        )
