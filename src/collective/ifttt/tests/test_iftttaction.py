# -*- coding: utf-8 -*-
from collective.ifttt.actions.ifttt import IftttEditFormView
from collective.ifttt.actions.ifttt import IftttTriggerAction
from plone.app.testing.bbb import PloneTestCase
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleAction
from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.adapter import _decodeCookieValue
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface


@implementer(Interface)
class DummyEvent(object):
    pass


class IftttTests(PloneTestCase):
    def afterSetUp(self):
        self.setRoles(('Manager', ))
        self.request = self.layer['request']

    def test_action_registered(self):
        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        self.assertEqual('plone.actions.Ifttt', element.addview)
        self.assertEqual('edit', element.editview)
        self.assertEqual('Ifttt Trigger Action', element.title)

    def test_addview(self):
        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        rule = self.portal.restrictedTraverse('++rule++foo')

        adding = getMultiAdapter((rule, self.request), name='+action')
        addview = getMultiAdapter((adding, self.request), name=element.addview)

        addview.form_instance.update()
        content = addview.form_instance.create(
            data={
                'message': 'Trigger Ifttt',
                'message_type': 'info'
            }
        )
        addview.form_instance.add(content)

        e = rule.actions[0]
        self.assertTrue(isinstance(e, IftttTriggerAction))
        self.assertEqual('Trigger Ifttt', e.message)
        self.assertEqual('info', e.message_type)

    def test_editview(self):
        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        e = IftttTriggerAction()
        editview = getMultiAdapter((e, self.request), name=element.editview)
        self.assertTrue(isinstance(editview, IftttEditFormView))

    def test_action_executor(self):
        e = IftttTriggerAction()
        e.message = 'Trigger Ifttt'
        e.message_type = 'info'

        ex = getMultiAdapter((self.folder, e, DummyEvent()), IExecutable)
        self.assertEqual(True, ex())

        new_cookies = self.request.RESPONSE.cookies[STATUSMESSAGEKEY]
        messages = _decodeCookieValue(new_cookies['value'])
        self.assertEqual(1, len(messages))
        self.assertEqual('Trigger Ifttt', messages[0].message)
        self.assertEqual('info', messages[0].type)
