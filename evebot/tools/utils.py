#!/usr/bin/env python3

"""
Because no project is complete without utils
 - Rocky Craig
"""


import logging
import os

from logging import handlers


def config_logger():
    log_path = '/var/tmp/eveslut'
    logger = logging.getLogger()
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    logger.setLevel(logging.DEBUG)
    file_handler = handlers.RotatingFileHandler(log_path)
    file_handler.doRollover()
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s %(levelname)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
