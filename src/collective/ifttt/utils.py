# -*- coding: utf-8 -*-
from collective.ifttt import _
from interfaces import IFTTTMarker
from plone import api
from plone.app.contentrules import api as rules_api
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IRuleCondition
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides


class Rules(object):
    """Define content rule operations within collective.ifttt environment"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        '''
        data should have keys
        ifttt_event_name, content_types, workflow_transitions  and payload
        '''

    def add_rule(self, data):
        '''
        Create new rule
        require data related to field values to create new rule
        '''

        # REDFINE ME
        rule_name = _(
            u'${title}_Trigger_${ifttt_event_name}',
            mapping=dict(
                ifttt_event_name=data.get('ifttt_event_name'),
                title=self.context.Title().decode('utf-8', 'ignore'),
            )
        )

        rule_description = _(
            u'This rule is created to trigger ${ifttt_event_name} '
            u'on ${title} folder',
            mapping=dict(
                ifttt_event_name=data.get('ifttt_event_name'),
                title=self.context.Title().decode('utf-8', 'ignore'),
            )
        )

        portal = api.portal.get()
        adding = getMultiAdapter((portal, self.request), name='+rule')

        addview = getMultiAdapter((adding, self.request),
                                  name='plone.ContentRule')
        addview.form_instance.update()
        content = addview.form_instance.create({
            'title': rule_name,
            'description': rule_description,
            'enabled': True,
            'stop': False,
            'cascading': False,
            'event': data.get('event')
        })
        addview.form_instance.add(content)

    def delete_rule(self):
        '''
        Delete rule
        '''

        # rule_id = self.request['rule-id']
        # storage = getUtility(IRuleStorage)
        # del storage[rule_id]
        # return 'ok'

    def configure_rule(self, data):
        '''
        Add trigger and action conditions to newly created content rule
        '''

        storage = getUtility(IRuleStorage)

        # find the rule_id of newly created rule
        # HACK, last created rule is the required rule
        self.rule = storage.values()[-1]
        self.rule_id = self.rule.id

        # traverse to configuration page of content rule
        rule = api.portal.get().restrictedTraverse(self.rule_id)

        # add conditions to rule
        self.add_condition(data, rule)

        # add actions to rule
        self.add_action(data, rule)

    def add_condition(self, data, rule):
        '''
        Add condition to rule
        '''

        # add content_types conditions
        element = getUtility(
            IRuleCondition, name='plone.conditions.PortalType'
        )
        adding = getMultiAdapter((rule, self.request), name='+condition')
        addview = getMultiAdapter((adding, self.request), name=element.addview)

        for i in data.get('content_types', []):
            addview.form_instance.update()
            content = addview.form_instance.create(data={'check_types': [i]})
            addview.form_instance.add(content)

        # add workflow_transitions conditions
        element = getUtility(
            IRuleCondition, name='plone.conditions.WorkflowTransition'
        )
        adding = getMultiAdapter((rule, self.request), name='+condition')
        addview = getMultiAdapter((adding, self.request), name=element.addview)

        for i in data.get('workflow_transitions', []):
            addview.form_instance.update()
            content = addview.form_instance.create(
                data={'wf_transitions': [i]}
            )
            addview.form_instance.add(content)

        # add workflow_states condition
        element = getUtility(
            IRuleCondition, name='plone.conditions.WorkflowState'
        )
        adding = getMultiAdapter((rule, self.request), name='+condition')
        addview = getMultiAdapter((adding, self.request), name=element.addview)

        for i in data.get('workflow_states', []):

            addview.form_instance.update()
            content = addview.form_instance.create(data={'wf_states': [i]})
            addview.form_instance.add(content)

    def add_action(self, data, rule):
        '''
        Add actions to rule
        '''

        element = getUtility(IRuleAction, name='plone.actions.Ifttt')
        adding = getMultiAdapter((rule, self.request), name='+action')
        addview = getMultiAdapter((adding, self.request), name=element.addview)

        addview.form_instance.update()
        content = addview.form_instance.create(
            data={
                'ifttt_event_name': data.get('ifttt_event_name'),
                'payload_option': data.get('payload')
            }
        )
        addview.form_instance.add(content)

    def apply_rule(self):
        'Apply content rule to requested folder'

        self.true_rule_id = self.rule_id.split('+')[-1]

        # 'form.button.AddAssignment'
        rules_api.assign_rule(self.context, self.true_rule_id)

        # imprints IFTTT marker on rules
        alsoProvides(self.rule, IFTTTMarker)
