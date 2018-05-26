# -*- coding: utf-8 -*-

from collective.ifttt import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IIftttControlPanel(Interface):

    ifttt_secret_key = schema.TextLine(
        title=_(u'Secret Key'),
        description=_(u'Register Ifttt"s secret key'),
        required=False,
    )


class IftttControlPanelForm(RegistryEditForm):
    schema = IIftttControlPanel
    schema_prefix = 'ifttt'
    label = u'Ifttt Settings'


IftttControlPanelView = layout.wrap_form(
    IftttControlPanelForm, ControlPanelFormWrapper
)
