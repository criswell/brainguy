# -*- coding: utf-8 -*-

"""
    Brainguy's inner workings.
"""

import logging

from brainguy.config import Config

try:
    __setup
except:
    __setup = False

def update_logger():
    debug_level = 3
    format = '%(asctime)s-%(levelname)s | %(message)s'
    log_file = None
    c = Config()
    if c.C.has_option('main', 'log_level'):
        debug_level = c.C.get('main', 'log_level')
    if c.C.has_option('main', 'log_format'):
        format = c.C.get('main', 'log_format')
    if c.C.has_option('main', 'log_file'):
        log_file = c.C.get('main', 'log_file')

    log_level = logging.DEBUG

    if debug_level < 1:
        log_level = logging.CRITICAL
    elif debug_level == 1:
        log_level = logging.ERROR
    elif debug_level == 2:
        log_level = logging.WARNING
    elif debug_level == 3:
        log_level = logging.INFO

    logging.basicConfig(level=log_level, format=format)

if not __setup:
    update_logger()
    __setup = True
