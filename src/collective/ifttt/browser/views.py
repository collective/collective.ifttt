# -*- coding: utf-8 -*-
from collective.ifttt import _
from plone import api
from plone.contentrules.engine.interfaces import IRuleAssignable
from plone.contentrules.engine.interfaces import IRuleStorage
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary


class checkView(BrowserView):
    def check_iftttconfig(self):

        # check that we are on a folder where content rules can be assigned
        if not IRuleAssignable.providedBy(self.context):
            return False

        # checks that content rules are not globally disabled
        # from content rules control panel
        storage = queryUtility(IRuleStorage)
        if not storage.active:
            return False

        # check if IFTTT secret key is added
        secret_key = api.portal.get_registry_record('ifttt.ifttt_secret_key')
        if not secret_key:
            return False
        return True


@provider(IContextSourceBinder)
def availableTriggers(context):
    registry = getUtility(IRuleStorage)
    terms = []
    if registry is not None:
        for key, rule in registry.items():
            terms.append(
                SimpleVocabulary.createTerm(
                    rule, key.encode('utf-8'),
                    _(u'${title}', mapping=dict(title=rule.title))
                )
            )

    return SimpleVocabulary(terms)
