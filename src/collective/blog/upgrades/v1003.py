from collective.blog import logger
from plone import api
from Products.GenericSetup.tool import SetupTool


def recatalog_post_authors(setup_tool: SetupTool):
    """Recatalog Posts."""
    with api.env.adopt_roles(["Manager"]):
        brains = api.content.find(portal_type=["Post"])
        total = len(brains)
        logger.info(f"Recatalog {total} items")
        for brain in brains:
            obj = brain.getObject()
            obj.reindexObject(idxs=["post_authors"])
    logger.info("Reindexed post_authors")
