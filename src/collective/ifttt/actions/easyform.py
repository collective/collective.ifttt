# -*- coding: utf-8 -*-

from collective.easyform.actions import Action
from collective.easyform.actions import ActionFactory
from collective.ifttt import _
from interfaces.ifttt_easyform_adapter import IIFTTT
from plone.supermodel.exportimport import BaseHandler
from zope.interface import implementer


@implementer(IIFTTT)
class IFTTTTrigger(Action):
    """Action Executor for easyform IFTTT adapter"""

    def __init__(self, **kw):
        for i, f in IIFTTT.namesAndDescriptions():
            setattr(self, i, kw.pop(i, f.default))
        super(IFTTTTrigger, self).__init__(**kw)

    def onSuccess(self, fields, request):
        # send field data to IFTTT event and Execute IFTTTTrigger Action
        pass


IFTTTAction = ActionFactory(
    IFTTTTrigger, _(u'IFTTTTrigger'), 'collective.ifttt.easyformadapter'
)

IFTTTHandler = BaseHandler(IFTTTTrigger)
