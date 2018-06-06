# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
from OFS.SimpleItem import SimpleItem
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


logger = logging.getLogger('collective.ifttt')

payload_options = SimpleVocabulary([
    SimpleTerm(value=u'Description', title=_(u'Description of action')),
    SimpleTerm(value=u'Username', title=_(u'Username of Editor')),
    SimpleTerm(
        value=u'Event start date/time', title=_(u'Event Start Date/Time')
    ),
])


class IIftttTriggerAction(Interface):
    """
        Definition of the configuration available for a  Ifttt action
    """
    ifttt_name = schema.TextLine(
        title=_(u'IFTTT event name'),
        description=_(u'The IFTTT event name'),
        required=False,
    )

    payload_option = schema.Choice(
        title=_(u'Choose 2nd Payload'),
        vocabulary=payload_options,
        description=_(
            u'Choose whether the 3rd payload is Description, '
            u'Username of editor, or Event Start Date/time'
        ),
    )
    payload = schema.Text(
        title=_(u'Payload'),
        required=False,
        description=_(u'Provide input for chosen payload')
    )


@implementer(IIftttTriggerAction, IRuleElementData)
class IftttTriggerAction(SimpleItem):
    """
        The implementation of the action defined before
    """

    ifttt_name = u''
    payload_option = u''
    payload = u''

    element = 'plone.actions.Ifttt'

    @property
    def summary(self):
        return _(
            u'${ifttt_name} ${payload_option}',
            mapping=dict(
                ifttt_name=self.ifttt_name,
                payload_option=self.payload_option,
                payload=self.payload,
            ),
        )


EXECUTOR = ThreadPoolExecutor(max_workers=1)


@implementer(IExecutable)
@adapter(Interface, IIftttTriggerAction, Interface)
class IftttTriggerActionExecutor(object):
    """
        The executor for this action
    """
    timeout = 120

    def __init__(self, element):
        self.element = element

    def __call__(self, *args, **kwargs):
        r = self.element.request
        ifttt_name = self.element.ifttt_name
        payload_option = self.element.payload_option
        payload = self.element.payload
        try:
            EXECUTOR.submit(
                # Post HTTP request
                r.post,
                ifttt_name,
                payload_option,
                data=payload,
                timeout=self.timeout
            )
        except TypeError:
            logger.exception('Error calling Ifttt Trigger:')
        return True


class IftttAddForm(ActionAddForm):
    """
    An add form for the ifttt action
    """
    schema = IIftttTriggerAction
    label = _(u'Add Ifttt Trigger Action')
    description = _(
        u'An ifttt trigger action will execute HTTP POST with '
        u'interpolated  JSON payload.'
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
        u'An ifttt trigger action will execute HTTP POST with '
        u'interpolated  JSON payload.'
    )
    form_name = _(u'Configure element')


class IftttEditFormView(ContentRuleFormWrapper):
    form = IftttEditForm
