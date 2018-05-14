# this file exists only to modify package path.
# On windows, it seems that files are loaded alphabetically
# at least that's what I can see in the logs
import os
import sys
import logging
logger = logging.getLogger()
logger.setLevel(logging.getLevelName("DEBUG"))
logger.debug("0.py sys.path: %s" % sys.path)
folder = os.path.dirname(__file__)
if folder not in sys.path:
    logger.debug("added %s to sys.path" % folder)
    sys.path.insert(1, folder)
