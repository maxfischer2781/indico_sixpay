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
from ... import MODULE_ID


class RHEPaymentmodifSixPay(RHEPaymentModifBase):
    _requestTag = "modifSixPay"

    def _process(self):
        p = ePayments.WPConfModifEPaymentSixPay(self, self._conf)
        return p.display()


class RHEPaymentmodifSixPayDataModif(RHEPaymentModifBase):
    _requestTag = "modifSixPayData"

    def _process(self):
        p = ePayments.WPConfModifEPaymentSixPayDataModif(self, self._conf)
        return p.display()


class RHEPaymentmodifSixPayPerformDataModif(RHEPaymentModifBase):
    _requestTag = "modifSixPayPerformDataModif"

    def _checkParams(self, params):
        RHEPaymentModifBase._checkParams(self, params)
        self._cancel = params.has_key("cancel")

    def _process(self):
        if not self._cancel:
            ses = self._conf.getModPay().getPayModByTag(MODULE_ID)
            ses.setValues(self._getRequestParams())
        self._redirect(localUrlHandlers.UHConfModifEPaymentSixPay.getURL(self._conf))


class RHEPaymentconfirmSixPay(RHRegistrationFormDisplayBase):
    _requestTag = "effectuer"

    def _checkParams(self, params):
        RHRegistrationFormDisplayBase._checkParams(self, params)
        self._registrant = None
        regId = params.get("registrantId", "")
        if regId is not None:
            self._registrant = self._conf.getRegistrantById(regId)

    def _processIfActive(self):
        if self._registrant is not None:
            p = ePayments.WPconfirmEPaymentSixPay(self, self._conf, self._registrant)
            return p.display()


class RHEPaymentCancelSixPay(RHRegistrationFormDisplayBase):
    _requestTag = "annuler"

    def _checkParams(self, params):
        RHRegistrationFormDisplayBase._checkParams(self, params)
        self._registrant = None
        regId = params.get("registrantId", "")
        if regId is not None:
            self._registrant = self._conf.getRegistrantById(regId)

    def _processIfActive(self):
        if self._registrant is not None:
            p = ePayments.WPCancelEPaymentSixPay(self, self._conf, self._registrant)
            return p.display()


class RHEPaymentNotConfirmeSixPay(RHRegistrationFormDisplayBase):
    _requestTag = "noneffectuer"

    def _checkParams(self, params):
        RHRegistrationFormDisplayBase._checkParams(self, params)
        self._registrant = None
        regId = params.get("registrantId", "")
        if regId is not None:
            self._registrant = self._conf.getRegistrantById(regId)

    def _processIfActive(self):
        if self._registrant is not None:
            p = ePayments.WPNotconfirmEPaymentSixPay(self, self._conf, self._registrant)
            return p.display()


class RHEPaymentValideParamSixPay(RHConferenceBaseDisplay):
    _requestTag = "params"

    def _checkProtection(self):
        # Just bypass everything else, as we want the payment service
        # to acknowledge the payment
        pass

    def _checkParams(self, params):
        RHConferenceBaseDisplay._checkParams(self, params)
        self._regForm = self._conf.getRegistrationForm()
        self._params = params
        self._registrant = None
        regId = params.get("registrantId", "")
        if regId is not None:
            self._registrant = self._conf.getRegistrantById(regId)

    def _process(self):
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
