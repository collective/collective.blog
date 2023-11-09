"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import logging


PACKAGE_NAME = "collective_blog"

_ = MessageFactory("collective_blog")

logger = logging.getLogger("collective_blog")
