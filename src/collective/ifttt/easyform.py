# -*- coding: utf-8 -*-

from collective.easyform.actions import Action
from collective.easyform.actions import ActionFactory
from collective.easyform.interfaces import IAction
from collective.ifttt import _
from collective.ifttt.interfaces import IRequestsLibrary
from plone import api
from plone.supermodel.exportimport import BaseHandler
from zope import schema
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import implementer

import logging
import requests


logger = logging.getLogger('collective.ifttt')


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

    # send field data to IFTTT event and Execute IFTTTTrigger Action
    def onSuccess(self, fields, request):

        # check registry of ifttt secret key
        secret_key = api.portal.get_registry_record('ifttt.ifttt_secret_key')
        if not secret_key:
            api.portal.show_message(
                message=_(
                    u'Error calling IFTTT Trigger. '
                    u'Missing IFTTT secret key'
                ),
                request=getRequest(),
                type='info'
            )
            logger.info(
                'Error calling IFTTT Trigger. Missing IFTTT secret key'
            )
            return False

        payload = {}

        # get fields data as payload data
        for i in self.payload_fields:
            payload[i] = fields.get(i)

        # IFTTTActionExecutor
        timeout = 120
        ifttt_trigger_url = 'https://maker.ifttt.com/trigger/' + \
                            self.ifttt_event_name + '/with/key/' + secret_key

        # request handler
        r = queryMultiAdapter((self, getRequest()),
                              IRequestsLibrary,
                              default=requests)

        logger.info('Calling Post request to IFTTT')
        try:

            r.post(ifttt_trigger_url, data=payload, timeout=timeout)

            logger.info(
                'Successful Post request to IFTTT applet {0}'.format(
                    self.ifttt_event_name
                )
            )

        except TypeError:
            logger.exception(
                'Error calling IFTTT Trigger {0}'.format(
                    self.ifttt_event_name
                )
            )

        return True


IFTTTAction = ActionFactory(
    IFTTTTrigger, _(u'IFTTTTrigger'), 'collective.ifttt.easyformadapter'
)

IFTTTHandler = BaseHandler(IFTTTTrigger)
