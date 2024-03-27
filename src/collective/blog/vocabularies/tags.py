from collective.blog.utils import find_blog_container_uid
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class TermWithUrl(SimpleTerm):
    def __init__(self, value, url, token=None, title=None):
        super().__init__(value, token, title)
        self.url = url


@provider(IVocabularyFactory)
def tags_vocabulary(context):
    """Vocabulary of tags from the current blog."""
    terms = []
    blog_uid = find_blog_container_uid(context)
    if blog_uid:
        catalog = api.portal.get_tool("portal_catalog")
        brains = catalog.unrestrictedSearchResults(
            blog_uid=blog_uid, portal_type="BlogTag", sort_on="sortable_title"
        )
        for brain in brains:
            token = brain.UID
            title = brain.Title
            terms.append(TermWithUrl(token, brain.getURL(), token, title))
    return SimpleVocabulary(terms)
