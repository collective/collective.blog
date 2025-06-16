from collective.blog import logger
from plone import api
from Products.GenericSetup.tool import SetupTool


TYPES_MAPPING = (("Blog", "BlogFolder"),)


def _migrate_existing_content(old_pt: str, new_pt: str) -> int:
    """Update existing content items."""
    with api.env.adopt_roles(["Manager"]):
        # Search catalog as Manager
        brains = api.content.find(portal_type=old_pt)
        total = len(brains)
        logger.info(f"Convert {total} {old_pt} instances to {new_pt}")
        for brain in brains:
            obj = brain.getObject()
            obj.portal_type = new_pt
            obj.reindexObject()
        return total


def recatalog_portal_type(setup_tool: SetupTool):
    """Recatalog portal type for existing content items."""
    for old_pt, new_pt in TYPES_MAPPING:
        items = _migrate_existing_content(old_pt, new_pt)
        logger.info(f"Converted {items} {old_pt} instances")
    logger.info("Converted old Blog instances")


def recatalog_blog_uid(setup_tool: SetupTool):
    """Recatalog Post and Author blog_uid."""
    with api.env.adopt_roles(["Manager"]):
        brains = api.content.find(portal_type=["Author", "Post"])
        total = len(brains)
        logger.info(f"Recatalog {total} items")
        for brain in brains:
            obj = brain.getObject()
            obj.reindexObject(idxs=["blog_uid"])
    logger.info("Reindexed blog_uid")
