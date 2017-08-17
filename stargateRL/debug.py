"""Logging and debugging utilities."""

import logging

from stargateRL.paths import FilePaths

# CRITICAL  50
# ERROR     40
# WARNING   30
# INFO      20
# DEBUG     10
# NOTSET    0

# TODO: Add stdout logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

_handler = logging.FileHandler(FilePaths.LOG.value)
_handler.setLevel(logging.DEBUG)

_ft = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
_handler.setFormatter(_ft)

logger.addHandler(_handler)

if __name__ == '__main__':
    logger.info('Started logging')
