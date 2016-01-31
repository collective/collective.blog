# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.blog


class CollectiveBlogLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.blog)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.blog:default')


COLLECTIVE_BLOG_FIXTURE = CollectiveBlogLayer()


COLLECTIVE_BLOG_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_BLOG_FIXTURE,),
    name='CollectiveBlogLayer:IntegrationTesting'
)


COLLECTIVE_BLOG_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_BLOG_FIXTURE,),
    name='CollectiveBlogLayer:FunctionalTesting'
)


COLLECTIVE_BLOG_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_BLOG_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveBlogLayer:AcceptanceTesting'
)
