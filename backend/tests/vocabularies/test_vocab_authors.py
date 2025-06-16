from collective.blog import PACKAGE_NAME
from plone import api
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabAuthors:
    name = f"{PACKAGE_NAME}.authors"

    @pytest.fixture(autouse=True)
    def _init(self, get_vocabulary, portal, authors):
        for authors_uid in authors:
            obj = api.content.find(UID=authors_uid)[0].getObject()
            obj.reindexObject()
        self.vocab = get_vocabulary(self.name, portal["tech-blog"])

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "value",
        [
            "Douglas Adams",
            "Marvin",
        ],
    )
    def test_titles(self, value: str):
        titles = [term.title for term in self.vocab._terms]
        assert value in titles

    def test_excludes_authors_from_another_blog(self, get_vocabulary, portal):
        api.content.create(
            type="Author",
            container=portal.dumpster.authors,
            title="Ford Prefect",
        )
        vocab = get_vocabulary(self.name, portal)
        titles = [term.title for term in vocab._terms]
        assert "Ford Prefect" not in titles
