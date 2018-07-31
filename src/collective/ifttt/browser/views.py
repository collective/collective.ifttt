# -*- coding: utf-8 -*-
from collective.ifttt import _
from collective.ifttt.interfaces import IFTTTMarker
from plone import api
from plone.contentrules.engine.interfaces import IRuleAssignable
from plone.contentrules.engine.interfaces import IRuleAssignmentManager
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

    # get rules assigned to context
    assignable = IRuleAssignmentManager(context)

    # get storage
    storage = getUtility(IRuleStorage)
    terms = []

    if storage and assignable is not None:

        # iterate over context rules
        for key, assignment in assignable.items():
            rule = storage.get(key, None)
            # check if given rule is an IFTTT rule
            if IFTTTMarker.providedBy(rule):
                terms.append(
                    SimpleVocabulary.createTerm(
                        rule, key.encode('utf-8'),
                        _(u'${title}', mapping=dict(title=rule.title))
                    )
                )

    return SimpleVocabulary(terms)
