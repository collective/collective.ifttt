# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.stringinterp.interfaces import IStringInterpolator
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import json
import logging


logger = logging.getLogger('collective.ifttt')

methods = SimpleVocabulary([
    SimpleTerm(value=u'GET', title=_(u'GET')),
    SimpleTerm(value=u'POST', title=_(u'POST')),
])


class IIftttAction(Interface):
    """
        Definition of the configuration available for a  Ifttt action
    """
    ifttt_name = schema.Text(
        title=_(u'IFTTT event name'),
        description=_(u'The IFTTT event name'),
        required=False,
    )

    method = schema.Choice(
        title=_(u'Call method'),
        vocabulary=methods,
    )

    payload = schema.Text(
        title=_(u'Payload'),
        description=_(
            u'Whether the 3rd payload is Description, '
            u'Username of editor, or Event Start Date/time'
        ),
        required=False,
    )


@implementer(IIftttAction, IRuleElementData)
class IftttAction(SimpleItem):
    """
        The implementation of the action defined before
    """

    ifttt_name = u''
    method = u''
    payload = u''

    element = 'plone.actions.Ifttt'

    @property
    def summary(self):
        return _(
            u'${method} ${ifttt_name}',
            mapping=dict(method=self.method, ifttt_name=self.ifttt_name),
        )


def interpolate(value, interpolator):
    """Recursively interpolate supported values"""
    if isinstance(value, unicode):
        return interpolator(value).strip()
    elif isinstance(value, list):
        return [interpolate(v, interpolator) for v in value]
    elif isinstance(value, dict):
        return dict([(k, interpolate(v, interpolator))
                     for k, v in value.items()])
    return value


EXECUTOR = ThreadPoolExecutor(max_workers=1)


@implementer(IExecutable)
@adapter(Interface, IIftttAction, Interface)
class IftttActionExecutor(object):
    """
        The executor for this action
    """
    timeout = 120

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self, *args, **kwargs):
        method = self.element.method
        r = self.element.request
        obj = self.event.object
        ifttt_name = self.element.ifttt_name
        interpolator = IStringInterpolator(obj)
        payload = interpolator(json.loads(self.element.payload), interpolator)
        try:
            if method == 'POST':
                payload = json.dumps(payload)
                EXECUTOR.submit(
                    r.post, ifttt_name, data=payload, timeout=self.timeout
                )
            elif method == 'GET':
                for key in payload:
                    payload[key] = json.dumps(payload[key]).strip('"')
                EXECUTOR.submit(
                    r.get, ifttt_name, params=payload, timeout=self.timeout
                )
        except TypeError:
            logger.exception('Error calling Ifttt:')
        return True


class IftttAddForm(ActionAddForm):
    """
    An add form for the ifttt action
    """
    schema = IIftttAction
    label = _(u'Add Ifttt Action')
    description = _(
        u'An ifttt action can execute HTTP GET or POST with '
        u'interpolated  JSON payload.'
    )
    form_name = _(u'Configure element')
    Type = IftttAction
    # template = ViewPageTemplateFile(os.path.join('templates', 'ifttt.pt'))


class IftttAddFormView(ContentRuleFormWrapper):
    form = IftttAddForm


class IftttEditForm(ActionEditForm):
    """
    An edit form for the ifttt action
    z3c.form does all the magic here.
    """
    schema = IIftttAction
    label = _(u'Edit Ifttt Action')
    description = _(
        u'An ifttt action can execute HTTP GET or POST with '
        u'interpolated  JSON payload.'
    )
    form_name = _(u'Configure element')
    # template = ViewPageTemplateFile(os.path.join('templates', 'ifttt.pt'))


class IftttEditFormView(ContentRuleFormWrapper):
    form = IftttEditForm
