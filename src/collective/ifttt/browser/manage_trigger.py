# -*- coding: utf-8 -*-

from collective.ifttt import _
from plone import api
from plone.autoform import directives as forms
from plone.autoform.form import AutoExtensibleForm
from plone.contentrules.engine.interfaces import IRuleStorage
from views import availableTriggers
from z3c.form import button
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import Interface

import logging


logger = logging.getLogger('collective.ifttt')


class ManageTriggerSchema(Interface):
    '''Define schema for manage IFTTT Trigger form'''

    forms.widget('ifttt_triggers', CheckBoxFieldWidget)
    ifttt_triggers = schema.Tuple(
        title=_(u'IFTTT Triggers'),
        description=_(u'Select certain IFTTT Triggers to delete'),
        required=False,
        missing_value=None,
        default=(),
        value_type=schema.Choice(source=availableTriggers)
    )


class ManageTrigger(AutoExtensibleForm, form.Form):
    '''
    Define Form
    '''

    schema = ManageTriggerSchema
    ignoreContext = True
    form_name = 'manage_trigger'

    label = _(u'Manage IFTTT Triggers')
    description = _(u'IFTTT triggers that are set on folder')

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(ManageTrigger, self).update()

    @button.buttonAndHandler(_(u'Delete'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        try:
            # delete the requested triggers

            rules = data.get('ifttt_triggers')
            storage = getUtility(IRuleStorage)
            for rule in rules:
                del storage[rule.id.split('+')[-1]]

            # Redirect back to the front page with a status message

            api.portal.show_message(
                message=_(
                    u'Successfully applied changes',
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
                message=_(u'Error'), request=getRequest(), type='info'
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
