# -*- coding: utf-8 -*-

from collective.ifttt.testing import COLLECTIVE_IFTTT_INTEGRATION_TESTING
from zope.component import getMultiAdapter

import unittest


class TestControlPanelView(unittest.TestCase):

    layer = COLLECTIVE_IFTTT_INTEGRATION_TESTING

    def setUp(self):
        """utility setup for tests"""

        self.context = self.layer['portal']
        self.request = self.layer['request']
        self.view = getMultiAdapter((self.context, self.request),
                                    name='collectiveifttt-controlpanel')

    # Test existence of ControlPanel

    def test_controlpanel(self):

        controlpanel_view = self.view()
        self.assertIn('Register an IFTTT secret key', controlpanel_view)
