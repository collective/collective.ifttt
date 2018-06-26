# -*- coding: utf-8 -*-

from collective.ifttt import _
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleCondition
from Products.CMFCore.interfaces._events import IActionSucceededEvent
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import Interface

import logging


logger = logging.getLogger('collective.ifttt')


class AddRuleSchema(Interface):
    '''
        Define schema for add rule form
        '''

    ifttt_event_name = schema.TextLine(
        title=_(u'IFTTT event name'),
        description=_(
            u'Give the name of IFTTT event which you want to trigger'
        ),
        required=True,
    )

    content_types = schema.Tuple(
        title=_(u'Content Types'),
        description=_(
            u'Select certain content types which should be restricted '
            u'to this event'
        ),
        required=False,
        missing_value=None,
        default=(),
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes'
        )
    )

    workflow_transitions = schema.Tuple(
        title=_(u'Workflow Transitions'),
        description=_(
            u'Select certain workflow transitions which should be restricted'
            u' to this event'
        ),
        required=False,
        missing_value=None,
        default=(),
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.WorkflowTransitions'
        )
    )


class AddRule(AutoExtensibleForm, form.Form):
    '''
    Define Form
    '''

    schema = AddRuleSchema
    ignoreContext = True
    form_name = 'add_ifttt_rule'

    label = _(u'Add new IFTTT trigger')
    description = _(u'This will add new IFTTT Trigger')

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(AddRule, self).update()

    @button.buttonAndHandler(_(u'Add'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        try:
            # all the backend magic goes here

            self.add_rule(data)

            self.configure_rule(data)

            # Redirect back to the front page with a status message

            api.portal.show_message(
                message=_(
                    u'Successfully applied the IFTTT event '
                    u'${ifttt_event_name} to ${title}',
                    mapping=dict(
                        ifttt_event_name=data['ifttt_event_name'],
                        title=self.context.Title().decode('utf-8', 'ignore'),
                    ),
                ),
                request=getRequest(),
                type='info'
            )

        except Exception as er:

            logger.exception(
                u'Unexpected exception: {0:s}'.format(er),
            )  # noqa

            # Redirect back to the front page with a status message

            api.portal.show_message(
                message=_(u'Error calling IFTTT Trigger'),
                request=getRequest(),
                type='info'
            )

        finally:

            contextURL = self.context.absolute_url()
            self.request.response.redirect(contextURL)

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

    def add_rule(self, data):
        '''
        Create new rule
        require data related to field values to create new rule
        '''

        # HACK
        rule_name = _(
            u'${title}_Trigger_${ifttt_event_name}',
            mapping=dict(
                ifttt_event_name=data['ifttt_event_name'],
                title=self.context.Title().decode('utf-8', 'ignore'),
            )
        )

        rule_description = _(
            u'This rule is created to trigger ${ifttt_event_name} '
            u'on ${title} folder',
            mapping=dict(
                ifttt_event_name=data['ifttt_event_name'],
                title=self.context.Title().decode('utf-8', 'ignore'),
            )
        )

        # HACK
        adding = self.context.restrictedTraverse('/Plone/+rule')

        addview = getMultiAdapter((adding, self.request),
                                  name='plone.ContentRule')
        addview.form_instance.update()
        content = addview.form_instance.create({
            'title':
            rule_name,
            'description':
            rule_description,
            'enabled':
            True,
            'stop':
            False,
            'cascading':
            False,
            'event':
            IActionSucceededEvent
        })  # noqa
        addview.form_instance.add(content)

    def delete_rule(self):
        '''
        Delete rule
        '''

    #     rule_id = self.request['rule-id']
    #     storage = getUtility(IRuleStorage)
    #     del storage[rule_id]
    #     return 'ok'

    def configure_rule(self, data):
        '''
        Add trigger and action conditions to newly created content rule
        '''

        storage = getUtility(IRuleStorage)

        # find the rule_id of newly created rule
        # HACK, last created rule is the required rule
        rule_id = storage.values()[-1].id

        # traverse to configuration page of content rule
        rule_url = '/Plone/' + rule_id
        adding = self.context.restrictedTraverse(rule_url)

        # add conditions to rule
        self.add_condition(data, adding)

        # add actions to rule
        self.add_action(data, adding)

    def add_condition(self, data, adding):
        '''
        Add condition to rule
        '''

        # add content_types conditions
        element = getUtility(
            IRuleCondition, name='plone.conditions.PortalType'
        )
        addview = getMultiAdapter((adding, self.request), name='+condition')
        addview = getMultiAdapter((addview, self.request),
                                  name=element.addview)

        for i in data['content_types']:
            addview.form_instance.update()
            content = addview.form_instance.create(data={'check_types': [i]})
            addview.form_instance.add(content)

        # add workflow_transitions conditions
        element = getUtility(
            IRuleCondition, name='plone.conditions.WorkflowTransition'
        )
        addview = getMultiAdapter((adding, self.request), name='+condition')
        addview = getMultiAdapter((addview, self.request),
                                  name=element.addview)

        for i in data['workflow_transitions']:
            addview.form_instance.update()
            content = addview.form_instance.create(
                data={'wf_transitions': [i]}
            )
            addview.form_instance.add(content)

    def add_action(self, data, adding):
        '''
        Add actions to rule
        '''
