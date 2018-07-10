# -*- coding: utf-8 -*-

from collective.ifttt import _
from collective.ifttt.actions.ifttt import PAYLOAD_USERNAME
from collective.ifttt.utils import Rules
from plone import api
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.globalrequest import getRequest
from zope.interface import Interface
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

import logging


logger = logging.getLogger('collective.ifttt')


class UserTriggerSchema(Interface):
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


class UserTrigger(AutoExtensibleForm, form.Form):
    '''
    Define Form
    '''

    schema = UserTriggerSchema
    ignoreContext = True
    form_name = 'user_content_trigger'

    label = _(u'Add new Content and User Trigger')
    description = _(
        u'This will send a trigger to IFTTT when content '
        u'at or below the current path is edited, including '
        u'the information of who changed it. '
    )

    def update(self):
        # disable Plone's editable border
        self.request.set('disable_border', True)

        # call the base class version - this is very important!
        super(UserTrigger, self).update()

    @button.buttonAndHandler(_(u'Add'))
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        try:
            # all the backend magic goes here
            '''
            available keys for data
            ifttt_event_name, content_types, workflow_transitions,
            payload, workflow_states
            and trigger event
            '''

            data['payload'] = PAYLOAD_USERNAME

            data['event'] = IObjectModifiedEvent

            rule = Rules(self.context, self.request)

            rule.add_rule(data)

            rule.configure_rule(data)

            rule.apply_rule()

            # Redirect back to the front page with a status message

            api.portal.show_message(
                message=_(
                    u'Successfully applied the IFTTT event '
                    u'${ifttt_event_name} to ${title}',
                    mapping=dict(
                        ifttt_event_name=data.get('ifttt_event_name'),
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
