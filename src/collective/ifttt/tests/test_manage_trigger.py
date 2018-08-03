# -*- coding: utf-8 -*-
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
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
        # Check existence of Manage IFTTT Trigger Action Menu

        self.view = getMultiAdapter((self.portal, self.request),
                                    name='ifttt_manage_trigger')
        actions_view = self.view()
        self.assertIn('Select certain IFTTT Triggers to delete', actions_view)

    def test_manage(self):

        self.request.method = 'POST'

        # add a test trigger
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

        # test ifttt_manage interface
        self.request.form = {}
        # ERROR: storage value is not reached to manager
        self.request.form['form.widgets.ifttt_triggers'] = ['rule-1']
        self.request.form['form.buttons.delete'] = u'Delete'
        self.view = getMultiAdapter((self.portal, self.request),
                                    name='ifttt_manage_trigger')
        self.view()

        storage = getUtility(IRuleStorage)

        # check that rule has been successfully deleted
        self.assertEqual(0, len(storage.values()))
