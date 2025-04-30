from collective.blog.utils import find_blog_container_uid
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def authors_vocabulary(context):
    """Vocabulary of authors from the current blog."""
    terms = []
    blog_uid = find_blog_container_uid(context)
    if blog_uid:
        brains = api.content.find(
            blog_uid=blog_uid, portal_type="Author", sort_on="sortable_title"
        )
        for brain in brains:
            token = brain.UID
            title = brain.Title
            terms.append(SimpleTerm(token, token, title))
    return SimpleVocabulary(terms)
