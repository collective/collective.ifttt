# -*- coding: utf-8 -*-
from collective.ifttt import _
from collective.ifttt.interfaces import IRequestsLibrary
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.event.interfaces import IEventAccessor
from zope import schema
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging
import requests


logger = logging.getLogger('collective.ifttt')

PAYLOAD_DESCRIPTION = 'description'
PAYLOAD_USERNAME = 'username'
PAYLOAD_START = 'start'

payload_options = SimpleVocabulary([
    SimpleTerm(
        value=PAYLOAD_DESCRIPTION, title=_(u'Description/Summary of content')
    ),
    SimpleTerm(value=PAYLOAD_USERNAME, title=_(u'Username of Editor')),
    SimpleTerm(value=PAYLOAD_START, title=_(u'Event Start Date/Time'))
])


class IIftttTriggerAction(Interface):
    """
        Definition of the configuration available for a  Ifttt action
    """
    ifttt_event_name = schema.TextLine(
        title=_(u'IFTTT event name'),
        description=_(
            u'Give the name of IFTTT event which you want to trigger'
        ),
        required=True,
    )

    payload_option = schema.Choice(
        title=_(u'Choose 3rd Payload'),
        vocabulary=payload_options,
        description=_(
            u'Choose whether the 3rd payload is Description of Content rule, '
            u'Username of editor, or Event Start Date/time'
        ),
        required=True,
    )


@implementer(IIftttTriggerAction, IRuleElementData)
class IftttTriggerAction(SimpleItem):
    """
        The implementation of the action defined before
    """

    ifttt_event_name = u''
    payload_option = u''

    element = 'plone.actions.Ifttt'

    @property
    def summary(self):
        return _(
            u'Trigger IFTTT action ${ifttt_event_name} with context title,'
            u'url and ${payload_option}',
            mapping=dict(
                ifttt_event_name=self.ifttt_event_name,
                payload_option=self.payload_option,
            ),
        )


@implementer(IExecutable)
@adapter(Interface, IIftttTriggerAction, Interface)
class IftttTriggerActionExecutor(object):
    """
        The executor for this action
    """
    timeout = 120

    # element is defined with Ifttt Trigger form
    # context is defined as site content for which content rule is triggered
    def __init__(self, context, element, event):
        self.element = element
        self.context = context
        self.event = event

    def __call__(self, *args, **kwargs):
        ifttt_event_name = self.element.ifttt_event_name
        payload_option = self.element.payload_option
        title = self.context.Title().decode('utf-8', 'ignore')
        url = self.context.absolute_url()
        secret_key = api.portal.get_registry_record('ifttt.ifttt_secret_key')
        ifttt_trigger_url = 'https://maker.ifttt.com/trigger/' + \
                            ifttt_event_name + '/with/key/' + secret_key
        payload = {'title': title, 'url': url}

        # define 3rd payload as chosen by user
        if payload_option == PAYLOAD_DESCRIPTION:
            payload[payload_option] = self.context.description
        elif payload_option == PAYLOAD_USERNAME:
            payload[payload_option] = api.user.get_current().getId()
        elif payload_option == PAYLOAD_START:
            try:
                '''
                This is a new contract in Plone 5 to allow any content that
                wants to behave like an event to define its start date & time,
                also decoupling it from the actual storage of the data.
                This also works for recurring events,
                because their start date & time should dynamically adapt to the
                next occurrence.
                '''
                payload[payload_option] = IEventAccessor(self.context).start
            except TypeError:
                '''
                when the context does implement or have
                registered adapter for IEventAccessor interface/contract
                '''
                payload[payload_option] = None
        '''we expect default behaviour here until
        indirection interface is needed to call IFTTT'''
        r = queryMultiAdapter((self.element, getRequest()),
                              IRequestsLibrary,
                              default=requests)

        logger.info('Calling Post request to IFTTT')
        try:

            r.post(ifttt_trigger_url, data=payload, timeout=self.timeout)

            # show this logging message to Plone user as notification
            api.portal.show_message(
                message=_(
                    u'Successfully triggered the IFTTT applet '
                    u'${ifttt_event_name}',
                    mapping=dict(ifttt_event_name=ifttt_event_name, ),
                ),
                request=getRequest(),
                type='info'
            )
            logger.info('Successful Post request to IFTTT')

        except TypeError:
            logger.exception('Error calling IFTTT Trigger')

            # show this logging message to Plone user as notification
            api.portal.show_message(
                message=_(
                    u'Error calling IFTTT Trigger',
                ),
                request=getRequest(),
                type='info'
            )

        return True


class IftttAddForm(ActionAddForm):
    """
    An add form for the ifttt action
    """
    schema = IIftttTriggerAction
    label = _(u'Add IFTTT Trigger')
    description = _(
        u'An IFTTT trigger action will execute POST request to IFTTT'
    )
    form_name = _(u'Configure element')
    Type = IftttTriggerAction


class IftttAddFormView(ContentRuleFormWrapper):
    form = IftttAddForm


class IftttEditForm(ActionEditForm):
    """
    An edit form for the ifttt action
    z3c.form does all the magic here.
    """
    schema = IIftttTriggerAction
    label = _(u'Edit IFTTT Action')
    description = _(
        u'An IFTTT trigger action will execute POST request to IFTTT'
    )
    form_name = _(u'Configure element')


class IftttEditFormView(ContentRuleFormWrapper):
    form = IftttEditForm
