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
            obj.reindexObject(
                idxs=[
                    "portal_type",
                    "Type",
                ],
            )
        return total


def recatalog_portal_type(setup_tool: SetupTool):
    """Recatalog portal type for existing content items."""
    for old_pt, new_pt in TYPES_MAPPING:
        items = _migrate_existing_content(old_pt, new_pt)
        logger.info(f"Converted {items} {old_pt} instances")
    logger.info("Upgrade complete")
