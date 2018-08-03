# -*- coding: utf-8 -*-

from collective.easyform.actions import Action
from collective.easyform.actions import ActionFactory
from collective.easyform.interfaces import IAction
from collective.ifttt import _
from plone.supermodel.exportimport import BaseHandler
from zope import schema
from zope.interface import implementer


class IIFTTT(IAction):
    """IFTTT action adapter on easyform that
    will send form fields data to IFTTT event."""

    ifttt_event_name = schema.TextLine(
        title=_(u'IFTTT event name'),
        description=_(
            u'Give the name of IFTTT event which you want to trigger '
            u'upon the successfull submission of easyform'
        ),
        required=True,
    )

    payload_fields = schema.List(
        title=_(u'Add Payloads'),
        description=_(
            u'Add upto 3 form fields to use as the payloads for IFTTT Trigger'
        ),
        unique=True,
        required=True,
        value_type=schema.Choice(vocabulary='easyform.Fields'),
        max_length=3
    )


@implementer(IIFTTT)
class IFTTTTrigger(Action):
    """Action Executor for easyform IFTTT adapter"""

    def __init__(self, **kw):
        for i, f in IIFTTT.namesAndDescriptions():
            setattr(self, i, kw.pop(i, f.default))
        super(IFTTTTrigger, self).__init__(**kw)

    def onSuccess(self, fields, request):
        # send field data to IFTTT event and Execute IFTTTTrigger Action
        pass


IFTTTAction = ActionFactory(
    IFTTTTrigger, _(u'IFTTTTrigger'), 'collective.ifttt.easyformadapter'
)

IFTTTHandler = BaseHandler(IFTTTTrigger)
