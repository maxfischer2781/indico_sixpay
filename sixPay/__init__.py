# -*- coding: utf-8 -*-
##
##
## This file is part of Indico.
## Copyright (C) 2002 - 2014 European Organization for Nuclear Research (CERN).
##
## Indico is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 3 of the
## License, or (at your option) any later version.
##
## Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Indico;if not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function
import sys

__metadata__ = {
    'type': "EPayment",
    'name': "SixPay"
    }

MODULE_ID = 'SixPay'

modules = {}

print('loaded sixPay', 'as', __name__, 'from', __file__)
import logging
six_logger = logging.getLogger('sixpay')
six_logger.propagate = False
_handler_file = logging.FileHandler('/tmp/sixpay.log')
_handler_file.setFormatter(logging.Formatter(fmt='#>>> %(asctime)s %(pathname)s::%(lineno)d[%(funcName)s]\n%(message)s'))
six_logger.addHandler(_handler_file)
_handler_stderr = logging.StreamHandler(sys.stderr)
_handler_stderr.setFormatter(logging.Formatter(fmt='  > %(pathname)s::%(lineno)d[%(funcName)s]\n%(message)s'))
six_logger.addHandler(_handler_stderr)
six_logger.setLevel(10)

six_logger.info('%s', 'loaded')
