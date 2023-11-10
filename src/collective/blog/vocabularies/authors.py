from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def authors_vocabulary(context):
    """Vocabulary of all authors."""
    terms = []
    brains = api.content.find(portal_type="Author", sort_on="sortable_title")
    for brain in brains:
        token = brain.UID
        title = brain.Title
        terms.append(SimpleTerm(token, token, title))
    return SimpleVocabulary(terms)
