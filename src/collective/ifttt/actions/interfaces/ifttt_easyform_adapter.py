# -*- coding: utf-8 -*-

from collective.easyform.interfaces import IAction
from collective.ifttt import _
from zope import schema


class IIFTTT(IAction):
    """IFTTT action adapter on easyform that
    will send form fields data to IFTTT event."""

    ifttt_event_name = schema.TextLine(
        title=_(u'IFTTT event name'),
        description=_(
            u'Give the name of IFTTT event which you want to trigger'
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
        value_type=schema.Choice(vocabulary='easyform.Fields')
        # TODO validate max input to 3
    )
