from collective.blog import PACKAGE_NAME
from plone import api
from zope.schema.vocabulary import SimpleVocabulary

import pytest


class TestVocabTags:
    name = f"{PACKAGE_NAME}.tags"

    @pytest.fixture(autouse=True)
    def _init(self, get_vocabulary, portal, tags):
        for tag_uid in tags:
            obj = api.content.find(UID=tag_uid)[0].getObject()
            obj.reindexObject()
        self.vocab = get_vocabulary(self.name, portal["tech-blog"])

    def test_vocabulary(self):
        assert self.vocab is not None
        assert isinstance(self.vocab, SimpleVocabulary)

    @pytest.mark.parametrize(
        "value",
        ["Retrocomputing"],
    )
    def test_titles(self, value: str):
        titles = [term.title for term in self.vocab._terms]
        assert value in titles

    def test_excludes_authors_from_another_blog(self, get_vocabulary, portal):
        api.content.create(
            type="BlogTag",
            container=portal.dumpster.tags,
            title="Androids",
        )
        vocab = get_vocabulary(self.name, portal["tech-blog"])
        titles = [term.title for term in vocab._terms]
        assert "Androids" not in titles
