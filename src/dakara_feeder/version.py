"""Version of the feeder."""

import logging

from packaging.version import parse

__version__ = "1.9.0-dev"
__date__ = "2022-11-23"

logger = logging.getLogger(__name__)


def check_version():
    """Display version number and check if on release."""
    # log player versio
    logger.info("Dakara feeder %s (%s)", __version__, __date__)

    # check version is a release
    version = parse(__version__)
    if version.is_prerelease:
        logger.warning("You are running a dev version, use it at your own risks!")
