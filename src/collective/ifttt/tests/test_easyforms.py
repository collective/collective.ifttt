# -*- coding: utf-8 -*-
from collective.easyform.api import get_actions
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from plone import api
from plone.app import testing
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from StringIO import StringIO
from zope.testing.loggingsupport import InstalledHandler
from ZPublisher.HTTPRequest import HTTPRequest
from ZPublisher.HTTPResponse import HTTPResponse

import plone.protect
import sys
import unittest


def FakeRequest(method='GET', add_auth=False, **kwargs):
    environ = {}
    environ.setdefault('SERVER_NAME', 'foo')
    environ.setdefault('SERVER_PORT', '80')
    environ.setdefault('REQUEST_METHOD', method)
    request = HTTPRequest(sys.stdin, environ, HTTPResponse(stdout=StringIO()))
    request.form = kwargs
    if add_auth:
        request.form['_authenticator'] = plone.protect.createToken()
    return request


class IFTTTTriggerTests(unittest.TestCase):

    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.folder = self.portal.portal_membership.getHomeFolder(
            testing.TEST_USER_ID
        )

        self.afterSetUp()

    def afterSetUp(self):
        api.content.create(
            container=self.portal,
            type='EasyForm',
            id='ff1',
        )
        self.ff1 = getattr(self.portal, 'ff1')

    def createIFTTTAction(self):

        # 1. Create IFTTT adapter in the form folder
        self.portal.REQUEST['form.widgets.title'] = u'Test IFTTT Adapter'
        self.portal.REQUEST['form.widgets.__name__'] = u'ifttt'
        self.portal.REQUEST['form.widgets.description'] = u''
        self.portal.REQUEST['form.widgets.factory'] = ['IFTTTTrigger']
        self.portal.REQUEST['form.buttons.add'] = u'Add'
        view = self.ff1.restrictedTraverse('actions/@@add-action')
        view.update()
        form = view.form_instance
        data, errors = form.extractData()
        self.assertEqual(len(errors), 0)

        # 2. Check that creation succeeded
        actions = get_actions(self.ff1)
        self.assertTrue('ifttt' in actions)

    def test_ActionExecutor(self):

        self.createIFTTTAction()

        # configure easyform actions
        self.assertTrue('ifttt' in get_actions(self.ff1))
        ifttt_trigger = get_actions(self.ff1)['ifttt']
        ifttt_trigger.ifttt_event_name = u'ifttt applet'
        ifttt_trigger.payload_fields = ['replyto', 'topic', 'comments']

        request = FakeRequest(
            add_auth=True,
            method='POST',
            topic='test subject',
            replyto='test@test.org',
            comments='test comments'
        )

        self.assertFalse(ifttt_trigger.onSuccess(request.form, request))

        # set secret key
        api.portal.set_registry_record(
            name='ifttt.ifttt_secret_key',
            value=u'secret',
        )

        # inspect logs
        handler = InstalledHandler('collective.ifttt.requests')

        # execute action
        self.assertTrue(ifttt_trigger.onSuccess(request.form, request))

        messages = [record.getMessage() for record in handler.records]
        self.assertGreater(len(messages), 0)
        self.assertTrue(messages[0].startswith('Dispatched requests.post'))
