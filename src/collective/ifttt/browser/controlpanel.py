# -*- coding: utf-8 -*-

from collective.ifttt import _
from collective.ifttt.interfaces import ICollectiveIFtttSettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout


class IftttControlPanelForm(RegistryEditForm):
    schema = ICollectiveIFtttSettings
    schema_prefix = 'ifttt'
    label = _(u'IFTTT Settings')


IftttControlPanelView = layout.wrap_form(
    IftttControlPanelForm, ControlPanelFormWrapper
)
