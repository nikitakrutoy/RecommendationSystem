#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import logging

MESSAGE_FORMAT ='[%(asctime)s] %(levelname)-8s : %(message)s'
DATE_FORMAT = '%y.%m.%d %H:%M:%S'


CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
DEBUG = logging.DEBUG


debug = logging.debug
info = logging.info
error = logging.error
critical = logging.critical


def level(level_name):
    return {
        'critical': CRITICAL,
        'error': ERROR,
        'debug': DEBUG
    }[level_name]


def config(level):
    logging.basicConfig(format=MESSAGE_FORMAT, level=level, datefmt=DATE_FORMAT)