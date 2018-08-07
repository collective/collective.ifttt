# -*- coding: utf-8 -*-
from collective.ifttt import _
from collective.ifttt.interfaces import IRequestsLibrary
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import collective.easyform
import collective.ifttt
import json
import logging


class CollectiveIftttLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.easyform)
        self.loadZCML(package=collective.ifttt)
        self.loadZCML(package=collective.ifttt, name='testing.zcml')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.easyform:default')
        applyProfile(portal, 'collective.ifttt:default')
        # noinspection PyProtectedMember
        portal.portal_setup._profile_upgrade_versions[
            'collective.ifttt:default'
        ] = (u'1000', )  # fake current profile version to allow upgrades


COLLECTIVE_IFTTT_FIXTURE = CollectiveIftttLayer()

COLLECTIVE_IFTTT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_IFTTT_FIXTURE, ),
    name='CollectiveIftttLayer:IntegrationTesting',
)

COLLECTIVE_IFTTT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_IFTTT_FIXTURE, ),
    name='CollectiveIftttLayer:FunctionalTesting',
)

COLLECTIVE_IFTTT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_IFTTT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveIftttLayer:AcceptanceTesting',
)


@implementer(IRequestsLibrary)
@adapter(Interface, Interface)
class RequestsLibraryMock(object):
    def __init__(self, element, request):
        self.element = element
        self.request = request
        self.logger = logging.getLogger('collective.ifttt.requests')

    def post(self, url, data=None, **kwargs):
        """Log request instead of posting it

        Log can be introspected in test by importing

            from zope.testing.loggingsupport import InstalledHandler

        registering a special loging handler before running the logging code

            handler = InstalledHandler('collective.ifttt.requests')

        and introspecting the handler data after code has been executed

            messages = [record.getMessage() for record in handler.records]
            self.assertGreater(len(messages), 0)
            self.assertTrue(messages[0].startswith('Dispatched requests.post'))

        """
        payload = data
        if isinstance(data, dict):
            payload = json.dumps(data)
        self.logger.info(
            u'Dispatched requests.post to {0:s}'
            u'with payload {1:s}.'.format(url, payload),
        )

        api.portal.show_message(
            message=_(
                u'Dispatched requests.post to ${url}'
                u'with payload ${payload}.',
                mapping=dict(url=url, payload=payload),
            ),
            request=self.request,
            type='info',
        )
