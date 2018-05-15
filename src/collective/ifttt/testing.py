# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.ifttt


class CollectiveIftttLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.ifttt)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.ifttt:default')


COLLECTIVE_IFTTT_FIXTURE = CollectiveIftttLayer()


COLLECTIVE_IFTTT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_IFTTT_FIXTURE,),
    name='CollectiveIftttLayer:IntegrationTesting',
)


COLLECTIVE_IFTTT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_IFTTT_FIXTURE,),
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
