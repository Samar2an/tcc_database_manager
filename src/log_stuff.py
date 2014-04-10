'''
################################################################################

log_stuff.py

    Provides the logging capabilities for other scripts here.  This makes it
    easy to modify the logging capabilities universally, as well as to keep the
    rest of the code cleaner.

################################################################################

COPYRIGHT (c) 2014 Marriott Library IT Services.  All Rights Reserved.

Author:          Pierce Darragh - pierce.darragh@utah.edu
Creation Date:   March 26, 2014
Last Updated:    March 26, 2014

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee is hereby granted, provided that
the above copyright notice appears in all copies and that both that copyright
notice and this permission notice appear in supporting documentation, and that
the name of The Marriott Library not be used in advertising or publicity
pertaining to distribution of the software without specific, written prior
permission. This software is supplied as-is without expressed or implied
warranties of any kind.

################################################################################
'''
import inspect
import logging
import logging.handlers

def build_logger (destination, name=None):
    '''Creates a well-formatted logger.  If a destination is specified, a RotatingFileHandler is used.
    '''

    toFile = True
    if destination == ''or not destination:
        toFile = False
    if not name:
        name = inspect.stack()[1][3]

    logger = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    level = logging.INFO

    if toFile:
        handler = logging.handlers.RotatingFileHandler(destination, maxBytes=102400, backupCount=5)
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logger.addHandler(handler)

    return logger
