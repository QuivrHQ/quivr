# encoding:utf-8

import logging
import sys

SWITCH = True

def _get_logger():
    log = logging.getLogger('log')
    log.setLevel(logging.INFO)
    console_handle = logging.StreamHandler(sys.stdout)
    console_handle.setFormatter(logging.Formatter('[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s',
                                                  datefmt='%Y-%m-%d %H:%M:%S'))
    log.addHandler(console_handle)
    return log

def close_log():
    global  SWITCH
    SWITCH = False


def debug(arg, *args):
    if SWITCH:
        if len(args) == 0:
            logger.debug(arg)
        else:
            logger.debug(arg.format(*args))

def info(arg, *args):
    if SWITCH:
        if len(args) == 0:
            logger.info(arg)
        else:
            logger.info(arg.format(*args))


def warn(arg, *args):
    if len(args) == 0:
        logger.warning(arg)
    else:
        logger.warning(arg.format(*args))

def error(arg, *args):
    if len(args) == 0:
        logger.error(arg)
    else:
        logger.error(arg.format(*args))

def exception(e):
    logger.exception(e)


logger = _get_logger()