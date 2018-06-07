# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from zope import schema
from zope.component import adapter
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
    SimpleTerm(value=PAYLOAD_DESCRIPTION, title=_(u'Description of action')),
    SimpleTerm(value=PAYLOAD_USERNAME, title=_(u'Username of Editor')),
    SimpleTerm(value=PAYLOAD_START, title=_(u'Event Start Date/Time'))
])


class IIftttTriggerAction(Interface):
    """
        Definition of the configuration available for a  Ifttt action
    """
    Title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title/Subject for action'),
        required=True,
    )

    URL = schema.URI(
        title=_(u'URL'),
        description=_(u'For files/images to view'),
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

    Title = u''
    URL = u''
    payload_option = u''

    element = 'plone.actions.Ifttt'

    @property
    def summary(self):
        return _(
            u'${Title} ${payload_option}',
            mapping=dict(
                Title=self.Title,
                URL=self.URL,
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

    def __init__(self, element, context, event):
        self.element = element
        self.context = context
        self.event = event

    def __call__(self, *args, **kwargs):
        Title = self.element.Title
        URL = self.element.URL
        payload_option = self.element.payload_option
        # TODO explore context and event; element is defined with Ifttt Trigger form
        # TODO define ifttt_url with secret key
        ifttt_name = self.event.title
        secret_key = self.event.secret_key
        ifttt_url = 'https://maker.ifttt.com/trigger/' + ifttt_name + '/with/key/' + secret_key
        # TODO define payload value
        payload = {'value1': Title, 'value2': URL, 'value3': ''}
        if payload_option == PAYLOAD_DESCRIPTION:
            payload['value3'] = self.event.description
        elif payload_option == PAYLOAD_USERNAME:
            payload['value3'] = api.user.get_users()
        elif payload_option == PAYLOAD_START:
            payload['value3'] = self.context.start
        logger.info('Calling Post request to Ifttt')
        try:
            # Post HTTP request
            requests.post(ifttt_url, data=payload, timeout=self.timeout)
            logger.info('Successful request call to Ifttt')
        except:
            logger.exception('Error calling Ifttt Trigger')
        return True


class IftttAddForm(ActionAddForm):
    """
    An add form for the ifttt action
    """
    schema = IIftttTriggerAction
    label = _(u'Add Ifttt Trigger Action')
    description = _(
        u'An ifttt trigger action will execute POST request to Ifttt'
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
    label = _(u'Edit Ifttt Action')
    description = _(
        u'An ifttt trigger action will execute POST request to Ifttt'
    )
    form_name = _(u'Configure element')


class IftttEditFormView(ContentRuleFormWrapper):
    form = IftttEditForm
