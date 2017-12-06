# -*- coding: utf-8 -*-
##
## This file is part of the SixPay Indico EPayment Plugin.
## Copyright (C) 2017 Max Fischer
##
## This is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 3 of the
## License, or (at your option) any later version.
##
## This software is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with SixPay Indico EPayment Plugin;if not, see <http://www.gnu.org/licenses/>.
from __future__ import unicode_literals

import urlparse
from xml.dom.minidom import parseString
from werkzeug.exceptions import NotImplemented as HTTPNotImplemented, InternalServerError as HTTPInternalServerError

import requests
from flask import flash, redirect, request
from flask_pluginengine import current_plugin
from werkzeug.exceptions import BadRequest

from indico.modules.events.payment.models.transactions import TransactionAction
from indico.modules.events.payment.notifications import notify_amount_inconsistency
from indico.modules.events.payment.util import register_transaction
from indico.modules.events.registration.models.registrations import Registration
from indico.web.flask.util import url_for
from indico.web.rh import RH

from .utility import gettext


class BaseRequestHandler(RH):
    """
    Request Handler for asynchronous callbacks from SixPay

    These handlers are used either by

    - the user, when he is redirected from SixPay back to Indico
    - SixPay, when it sends back the result of a transaction
    """
    CSRF_ENABLED = False

    def _process_args(self):
        self.token = request.args['token']
        self.registration = Registration.find_first(uuid=self.token)
        if not self.registration:
            raise BadRequest


class SixPayResponseHandler(BaseRequestHandler):
    """Handler for notification from SixPay service"""
    def _process(self):
        transaction_xml = request.form['DATA']
        transaction_signature = request.form['SIGNATURE']
        transaction_data = self._parse_transaction_xml(transaction_xml)
        if self._verify_signature(transaction_xml, transaction_signature, transaction_data['ID']):
            pass


    @staticmethod
    def _parse_transaction_xml(transaction_xml):
        """Parse the ``transaction_xml`` to a mapping"""
        mdom = parseString(transaction_xml)
        attributes = mdom.documentElement.attributes
        idp_data = {
            attributes.item(idx).name: attributes.item(idx).value
            for idx in range(attributes.length)
        }
        return idp_data

    @staticmethod
    def _verify_signature(transaction_xml, transaction_signature, transaction_id):
        """Verify the transaction data and signature with SixPay"""
        sixpay_url = current_plugin.settings.get('url')
        endpoint = urlparse.urljoin(sixpay_url, 'CreatePayInit.asp')
        url_request = requests.post(endpoint, DATA=transaction_xml, SIGNATURE=transaction_signature)
        # raise any HTTP errors
        url_request.raise_for_status()
        if url_request.text.startswith('ERROR'):
            raise HTTPInternalServerError('Failed request to SixPay service: %s' % url_request.text)
        elif url_request.text.startswith('OK'):
            # text = 'OK:ID=56a77rg243asfhmkq3r&TOKEN=%3e235462FA23C4FE4AF65'
            content = url_request.text.split(':', 1)[1]
            confirmation = dict(key_value.split('=') for key_value in content.split('&'))
            return confirmation['ID'] == transaction_id
        raise RuntimeError("Expected reply 'OK:ID=...&TOKEN=...', got %r" % url_request.text)

    def _check_duplicate_transaction(self, transaction_data):
        prev_transaction = self.registration.transaction
        if not prev_transaction or prev_transaction.provier != 'sixpay':
            return False
        return all(
            prev_transaction[key] == transaction_data[key]
            for key in ()
        )

class UserCancelHandler(BaseRequestHandler):
    """User Message on cancelled payment"""
    def _process(self):
        flash(_('You cancelled the payment process.'), 'info')
        return redirect(url_for('event_registration.display_regform', self.registration.locator.registrant))


class UserFailureHandler(BaseRequestHandler):
    """User Message on failed payment"""
    def _process(self):
        flash(_('Your payment request has failed.'), 'info')
        return redirect(url_for('event_registration.display_regform', self.registration.locator.registrant))


class UserSuccessHandler(SixPayResponseHandler):
    """User Message on successful payment"""
    def _process(self):
        flash(gettext('Your payment request has been processed.'), 'success')
        return redirect(url_for('event_registration.display_regform', self.registration.locator.registrant))
