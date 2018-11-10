# -*- coding: utf-8 -*-
from collective.ifttt.actions.ifttt import IftttEditFormView
from collective.ifttt.actions.ifttt import IftttTriggerAction
from collective.ifttt.actions.ifttt import payload_options
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from plone import api
from plone.app import testing
from plone.app.contentrules.rule import Rule
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.interfaces import IObjectEvent
from zope.interface import implementer
from zope.testing.loggingsupport import InstalledHandler

import unittest


@implementer(IObjectEvent)
class DummyEvent(object):
    def __init__(self, object):
        self.object = object


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
        self.assertEqual('IFTTT Trigger', element.title)

    def test_AddFormView(self):
        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        storage = getUtility(IRuleStorage)
        storage[u'ifttt_applet'] = Rule()
        rule = self.portal.restrictedTraverse('++rule++ifttt_applet')

        adding = getMultiAdapter((rule, self.portal.REQUEST), name='+action')
        addview = getMultiAdapter((adding, self.portal.REQUEST),
                                  name=element.addview)

        addview.form_instance.update()

        for index, option in enumerate(payload_options):

            content = addview.form_instance.create(
                data={
                    'ifttt_event_name': 'ifttt_applet',
                    'payload_option': option,
                }
            )
            addview.form_instance.add(content)

            e = rule.actions[index]
            self.assertTrue(isinstance(e, IftttTriggerAction))
            self.assertEqual('ifttt_applet', e.ifttt_event_name)
            self.assertEqual(option, e.payload_option)

    def test_EditFormView(self):
        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        e = IftttTriggerAction()
        editview = getMultiAdapter((e, self.portal.REQUEST),
                                   name=element.editview)
        self.assertTrue(isinstance(editview, IftttEditFormView))

    def test_ActionExecutor(self):

        element = IftttTriggerAction()
        context = self.portal.restrictedTraverse('')

        api.portal.set_registry_record(
            name='ifttt.ifttt_secret_key',
            value=u'secret',
        )
        element.ifttt_event_name = 'ifttt_applet'

        for option in payload_options:
            # inspect logs
            handler = InstalledHandler('collective.ifttt.requests')

            element.payload_option = option.value
            ex = getMultiAdapter((context, element, DummyEvent(self.folder)),
                                 IExecutable)
            self.assertTrue(ex())
            messages = [record.getMessage() for record in handler.records]
            self.assertGreater(len(messages), 0)
            self.assertTrue(messages[0].startswith('Dispatched requests.post'))
