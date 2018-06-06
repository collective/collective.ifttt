# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.interfaces import INonInstallable
from zope.component import getAllUtilitiesRegisteredFor

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.ifttt is properly installed."""

    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.setup = api.portal.get_tool('portal_setup')

    def test_product_installed(self):
        """Test if collective.ifttt is installed."""
        self.assertTrue(self.installer.isProductInstalled('collective.ifttt'))

    def test_product_upgrade(self):
        """Test if collective.ifttt can be upgraded."""
        self.assertIn(
            u'collective.ifttt:default',
            self.setup.listProfilesWithUpgrades(),
        )
        self.assertGreater(
            len(self.setup.listUpgrades(u'collective.ifttt:default')),
            0,
        )
        self.setup.upgradeProfile(u'collective.ifttt:default')
        self.assertEqual(
            len(self.setup.listUpgrades(u'collective.ifttt:default')),
            0,
        )

    def test_browserlayer(self):
        """Test that ICollectiveIftttLayer is registered."""
        from collective.ifttt.interfaces import (ICollectiveIftttLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveIftttLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.ifttt'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_hidden_uninstall_profile(self):
        """Test if uninstall profile is listed as hidden"""
        ignore_profiles = []
        utils = getAllUtilitiesRegisteredFor(INonInstallable)
        for util in utils:
            ignore_profiles.extend(util.getNonInstallableProfiles())
        self.assertIn(u'collective.ifttt:uninstall', ignore_profiles)

    def test_product_uninstalled(self):
        """Test if collective.ifttt is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('collective.ifttt'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveIftttLayer is removed."""
        from collective.ifttt.interfaces import \
            ICollectiveIftttLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveIftttLayer, utils.registered_layers())
