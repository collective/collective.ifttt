# -*- coding: utf-8 -*-
from collective.ifttt.actions.ifttt import IftttEditFormView
from collective.ifttt.actions.ifttt import IftttTriggerAction
from collective.ifttt.actions.ifttt import payload_options
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from plone.app import testing
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from zope.component import getMultiAdapter
from zope.component import getUtility

import unittest


class IftttTests(unittest.TestCase):

    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.folder = self.portal.portal_membership.getHomeFolder(
            testing.TEST_USER_ID
        )

    def test_action_registered(self):
        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        self.assertEqual('plone.actions.Ifttt', element.addview)
        self.assertEqual('edit', element.editview)
        self.assertEqual('IFTTT Trigger Action', element.title)

    def test_AddFormView(self):
        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        storage = getUtility(IRuleStorage)
        storage[u'ifttt_applet'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++ifttt_applet')

        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.form_instance.update()

        payload_option = payload_options.by_value.keys()

        for i in range(len(payload_option)):

            content = addview.form_instance.create(
                data={
                    'ifttt_event_name': 'ifttt_applet',
                    'payload_option': payload_option[i],
                }
            )
            addview.form_instance.add(content)

            e = rule.actions[i]
            self.assertTrue(isinstance(e, IftttTriggerAction))
            self.assertEqual('ifttt_applet', e.ifttt_event_name)
            self.assertEqual(payload_option[i], e.payload_option)

    def testInvokeEditView(self):
        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        e = IftttTriggerAction()
        editview = getMultiAdapter((e, self.portal.REQUEST),
                                   name=element.editview)
        self.assertTrue(isinstance(editview, IftttEditFormView))
