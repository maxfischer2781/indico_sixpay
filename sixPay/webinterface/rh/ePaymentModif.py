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

from MaKaC.webinterface.rh.ePaymentModif import RHEPaymentModifBase, RHConferenceBaseDisplay, RHRegistrationFormDisplayBase
import MaKaC.webinterface.urlHandlers as urlHandlers
from datetime import datetime
from MaKaC.common.timezoneUtils import nowutc


from ..pages import ePayments
from .. import urlHandlers as localUrlHandlers
from ... import epayment as ePayment
from ... import MODULE_ID, six_logger


# Editor's Note  - MF@20170309
# These classes implement the actual functionality. The URLHandlers link incoming
# request to RequestHandlers *by sharing the _requestTag field*. RequestHandlers
# actually digest data and modify state. They use the pages.ePayments to *display*
# results and data.


class RHEPaymentmodifSixPay(RHEPaymentModifBase):
    _requestTag = "modifSixPay"

    def _process(self):
        six_logger.info('%s', 'no parameters')
        p = ePayments.WPConfModifEPaymentSixPay(self, self._conf)
        return p.display()


class RHEPaymentmodifSixPayDataModif(RHEPaymentModifBase):
    _requestTag = "modifSixPayData"

    def _process(self):
        six_logger.info('%s', None)
        p = ePayments.WPConfModifEPaymentSixPayDataModif(self, self._conf)
        return p.display()


class RHEPaymentmodifSixPayPerformDataModif(RHEPaymentModifBase):
    _requestTag = "modifSixPayPerformDataModif"

    def _checkParams(self, params):
        six_logger.info('%s', params)
        RHEPaymentModifBase._checkParams(self, params)
        self._cancel = params.has_key("cancel")

    def _process(self):
        if not self._cancel:
            conference_six_epayment = self._conf.getModPay().getPayModByTag(MODULE_ID)
            data = self._getRequestParams()
            six_logger.info('%s', data)
            conference_six_epayment.setValues(data)
        self._redirect(localUrlHandlers.UHConfModifEPaymentSixPay.getURL(self._conf))


# Handlers for the Six Pay service to call back after/during a transaction
class RHTransactionUserCallback(RHRegistrationFormDisplayBase):
    """Request Handler for Callbacks the User is directed to"""
    #: display page after handling transaction
    display_page = None
    #: overwrite message on the displayed page
    message = None
    #: overwrite message detail on the displayed page
    message_detail = None

    def _checkParams(self, params):
        six_logger.info('%s', params)
        RHRegistrationFormDisplayBase._checkParams(self, params)
        self._registrant = None
        regId = params.get("registrantId", "")
        if regId is not None:
            self._registrant = self._conf.getRegistrantById(regId)

    def _processIfActive(self):
        six_logger.info('%s', 'no parameters')
        if self._registrant is not None:
            assert self.display_page is not None, "Callbacks must set display pages for users"
            display_page = self.display_page(self, self._conf, self._registrant)
            if self.message is not None:
                display_page.message = self.message
            if self.message_detail is not None:
                display_page.message_detail = self.message_detail
            six_logger.info('%s %s %s', self, display_page, self._registrant)
            return display_page.display()


class RHTransactionSuccesslink(RHTransactionUserCallback):
    """redirect when the user completed the transaction"""
    _requestTag = "successlink"
    display_page = ePayments.WPTransactionSuccesslink

    def _checkParams(self, params):
        six_logger.info('%s', params)
        # indico tries to evaluate the DATA xml as an HTML locator if we do not remove it
        data = params.pop('DATA')
        RHTransactionUserCallback._checkParams(self, params)
        conference_six_epayment = self._conf.getModPay().getPayModByTag(MODULE_ID)
        try:
            conference_six_epayment.verify_transaction(
                data=data,
                signature=params['SIGNATURE'],
                registrant=self._registrant,
            )
        except ePayment.TransactionError as transaction_error:
            self.message = "Your payment has been processed by SixPay, but a validation error occurred"
            self.message_detail = 'Please contact the event organizers to confirm your payment\n%s' % transaction_error


class RHTransactionFaillink(RHTransactionUserCallback):
    """redirect when the user could not be authorised"""
    _requestTag = "faillink"
    display_page = ePayments.WPTransactionFaillink


class RHTransactionBacklink(RHTransactionUserCallback):
    """redirect when the user aborts the transaction"""
    _requestTag = "backlink"
    display_page = ePayments.WPTransactionBacklink


# Handler called separate of user redirects after successfull transaction
# This sends the verification independent of any calls the user may or may not perform.
class RHTransactionNotifyUrl(RHTransactionSuccesslink):
    """endpoint for SixPay to confirm transaction WITHOUT user intervention"""
    _requestTag = "notifyurl"

    def _checkProtection(self):
        # Just bypass everything else, as we want the payment service
        # to acknowledge the payment
        pass

    def _process(self):
        # Everything has been handled by confirming the request, do not expose any more options
        pass


# TODO: remove old stuff
class RHEPaymentconfirmSixPay(RHRegistrationFormDisplayBase):
    _requestTag = "effectuer"

    def _checkParams(self, params):
        six_logger.info('%s', params)
        RHRegistrationFormDisplayBase._checkParams(self, params)
        self._registrant = None
        regId = params.get("registrantId", "")
        if regId is not None:
            self._registrant = self._conf.getRegistrantById(regId)

    def _processIfActive(self):
        six_logger.info('%s', None)
        if self._registrant is not None:
            p = ePayments.WPconfirmEPaymentSixPay(self, self._conf, self._registrant)
            return p.display()


class RHEPaymentCancelSixPay(RHRegistrationFormDisplayBase):
    _requestTag = "annuler"

    def _checkParams(self, params):
        six_logger.info('%s', params)
        RHRegistrationFormDisplayBase._checkParams(self, params)
        self._registrant = None
        regId = params.get("registrantId", "")
        if regId is not None:
            self._registrant = self._conf.getRegistrantById(regId)

    def _processIfActive(self):
        six_logger.info('%s', None)
        if self._registrant is not None:
            p = ePayments.WPCancelEPaymentSixPay(self, self._conf, self._registrant)
            return p.display()


class RHEPaymentNotConfirmeSixPay(RHRegistrationFormDisplayBase):
    _requestTag = "noneffectuer"

    def _checkParams(self, params):
        six_logger.info('%s', params)
        RHRegistrationFormDisplayBase._checkParams(self, params)
        self._registrant = None
        regId = params.get("registrantId", "")
        if regId is not None:
            self._registrant = self._conf.getRegistrantById(regId)

    def _processIfActive(self):
        six_logger.info('%s', None)
        if self._registrant is not None:
            p = ePayments.WPNotconfirmEPaymentSixPay(self, self._conf, self._registrant)
            return p.display()


class RHEPaymentValideParamSixPay(RHConferenceBaseDisplay):
    _requestTag = "params"

    def _checkProtection(self):
        six_logger.info('%s', None)
        # Just bypass everything else, as we want the payment service
        # to acknowledge the payment
        pass

    def _checkParams(self, params):
        six_logger.info('%s', params)
        RHConferenceBaseDisplay._checkParams(self, params)
        self._regForm = self._conf.getRegistrationForm()
        self._params = params
        self._registrant = None
        regId = params.get("registrantId", "")
        if regId is not None:
            self._registrant = self._conf.getRegistrantById(regId)

    def _process(self):
        six_logger.info('%s', None)
        regForm = self._conf.getRegistrationForm()
        if not regForm.isActivated() or not self._conf.hasEnabledSection("regForm"):
            p = regForm.WPRegFormInactive(self, self._conf)
            return p.display()
        else:
            if self._registrant is not None:
                self._registrant.setPayed(True)
                d = {
                    "ModPay": self._params.get(MODULE_ID),
                    "payment_date": nowutc(),
                    "TransactionID": self._params.get("txtTransactionID"),
                    "OrderTotal": self._params.get("txtOrderTotal"),
                    "Currency": self._params.get("txtArtCurrency"),
                    "PayMet": self._params.get("txtPayMet"),
                    "ESR_Member": self._params.get("txtESR_Member"),
                    "ESR_Ref": self._params.get("txtESR_Ref"),
                }
                trSixPay = ePayment.TransactionSixPay(d)
                self._registrant.setTransactionInfo(trSixPay)
                self._regForm.getNotification().sendEmailNewRegistrantConfirmPay(self._regForm, self._registrant)
