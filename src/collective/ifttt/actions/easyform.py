# -*- coding: utf-8 -*-

from collective.easyform.actions import Action
from collective.easyform.actions import ActionFactory
from collective.ifttt import _
from plone.supermodel.exportimport import BaseHandler


class IFTTTTrigger(Action):
    pass


IFTTTAction = ActionFactory(
    IFTTTTrigger, _(u'label_IFTTT_action', default=u'IFTTTTrigger'),
    'collective.ifttt.Addeasyformadapter'
)

IFTTTHandler = BaseHandler(IFTTTAction)
