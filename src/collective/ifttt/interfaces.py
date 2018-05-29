# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.ifttt import _
from plone.autoform import directives
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveIftttLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IIftttControlPanel(Interface):

    # A field in 'hidden' mode

    directives.mode(secret='hidden')
    ifttt_secret_key = schema.TextLine(
        title=_(u'Secret Key'),
        description=_(u'Register Ifttt"s secret key'),
    )
