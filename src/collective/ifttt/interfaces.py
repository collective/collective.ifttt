# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from collective.ifttt import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveIftttLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICollectiveIFtttSettings(Interface):

    # A field in 'hidden' mode

    ifttt_secret_key = schema.TextLine(
        title=_(u'Secret Key'),
        description=_(u'Register an IFTTT secret key'),
    )


class IRequestsLibrary(Interface):
    '''Indirection interface for adapting some context to requests library'''


class IFTTTMarker(Interface):
    """Marker interface for IFTTT"""
