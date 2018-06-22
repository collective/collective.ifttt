# -*- coding: utf-8 -*-

from collective.ifttt import _
from plone import api
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.globalrequest import getRequest
from zope.interface import Interface


class AddRuleSchema(Interface):
    '''
        Define schema for add rule form
        '''

    ifttt_event_name = schema.TextLine(
        title=_(u'IFTTT applet name'),
        description=_(
            u'Give the name of IFTTT applet which you want to trigger'
        ),
        required=True,
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

    @button.buttonAndHandler(_(u'ADD'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        try:
            # all the backend magic goes here

            # Redirect back to the front page with a status message

            api.portal.show_message(
                message=_(
                    u'Successfully applied the IFTTT applet '
                    u'${ifttt_event_name} to ${title}',
                    mapping=dict(
                        ifttt_event_name=data['ifttt_event_name'],
                        title=self.context.Title().decode('utf-8', 'ignore'),
                    ),
                ),
                request=getRequest(),
                type='info'
            )

        except TypeError:

            # Redirect back to the front page with a status message

            api.portal.show_message(
                message=_(u'Error calling IFTTT Trigger'),
                request=getRequest(),
                type='info'
            )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
