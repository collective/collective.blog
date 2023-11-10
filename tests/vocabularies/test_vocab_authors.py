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
        self.vocab = get_vocabulary(self.name, portal)

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
