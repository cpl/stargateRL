"""Logging and debugging utilities."""

import os
import logging

from stargateRL.paths import FilePaths

# CRITICAL  50
# ERROR     40
# WARNING   30
# INFO      20
# DEBUG     10
# NOTSET    0


def clear_log():
    """Remove the log file."""
    if os.path.isfile(FilePaths.LOG.value):
        os.remove(FilePaths.LOG.value)
    else:
        raise Exception('Log file does not exists.')


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
