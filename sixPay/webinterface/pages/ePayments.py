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

from MaKaC.webinterface.pages import conferences
from MaKaC.webinterface.pages import registrationForm
from MaKaC.webinterface import wcomponents
from xml.sax.saxutils import quoteattr
from indico.core import config as Configuration
from MaKaC.webinterface import urlHandlers
import MaKaC

from ..wcomponents import WTemplated
from .. import urlHandlers as localUrlHandlers
from ... import MODULE_ID


class WPConfModifEPaymentSixPayBase(registrationForm.WPConfModifRegFormBase):
    def _createTabCtrl(self):
        self._tabCtrl = wcomponents.TabControl()
        self._tabMain = self._tabCtrl.newTab(
            "main",
            "Main",
            localUrlHandlers.UHConfModifEPaymentSixPay.getURL(self._conf)
        )
        wf = self._rh.getWebFactory()
        if wf:
            wf.customiseTabCtrl(self._tabCtrl)
        self._setActiveTab()

    def _setActiveTab(self):
        pass

    def _setActiveSideMenuItem(self):
        self._regFormMenuItem.setActive(True)

    def _getPageContent(self, params):
        self._createTabCtrl()
        banner = wcomponents.WEpaymentBannerModif(self._conf.getModPay().getPayModByTag(MODULE_ID),
                                                  self._conf).getHTML()
        html = wcomponents.WTabControl(self._tabCtrl, self._getAW()).getHTML(self._getTabContent(params))
        return banner + html

    def _getTabContent(self, params):
        return "nothing"


class WPConfModifEPaymentSixPay(WPConfModifEPaymentSixPayBase):
    def _getTabContent(self, params):
        wc = WConfModifEPaymentSixPay(self._conf)
        p = {
            'dataModificationURL': quoteattr(
                str(localUrlHandlers.UHConfModifEPaymentSixPayDataModif.getURL(self._conf)))
        }
        return wc.getHTML(p)


class WConfModifEPaymentSixPay(WTemplated):
    def __init__(self, conference):
        self._conf = conference

    def getVars(self):
        vars = WTemplated.getVars(self)
        modSixPay = self._conf.getModPay().getPayModByTag(MODULE_ID)
        vars["title"] = modSixPay.getTitle()
        vars["url"] = modSixPay.getUrl()
        vars["shopid"] = modSixPay.getShopID()
        vars["mastershopid"] = modSixPay.getMasterShopID()
        vars["hashseed"] = modSixPay.getHashSeed()
        return vars


class WPConfModifEPaymentSixPayDataModif(WPConfModifEPaymentSixPayBase):
    def _getTabContent(self, params):
        wc = WConfModifEPaymentSixPayDataModif(self._conf)
        p = {'postURL': quoteattr(str(localUrlHandlers.UHConfModifEPaymentSixPayPerformDataModif.getURL(self._conf)))
             }
        return wc.getHTML(p)


class WConfModifEPaymentSixPayDataModif(WTemplated):
    def __init__(self, conference):
        self._conf = conference

    def getVars(self):
        vars = WTemplated.getVars(self)
        modSixPay = self._conf.getModPay().getPayModByTag(MODULE_ID)
        vars["title"] = modSixPay.getTitle()
        vars["url"] = modSixPay.getUrl()
        vars["shopid"] = modSixPay.getShopID()
        vars["mastershopid"] = modSixPay.getMasterShopID()
        vars["hashseed"] = modSixPay.getHashSeed()
        return vars


class WPconfirmEPaymentSixPay(conferences.WPConferenceDefaultDisplayBase):
    # navigationEntry = navigation.NERegistrationFormDisplay

    def __init__(self, rh, conf, reg):
        conferences.WPConferenceDefaultDisplayBase.__init__(self, rh, conf)
        self._registrant = reg

    def _getBody(self, params):
        wc = WconfirmEPaymentSixPay(self._conf, self._registrant)
        return wc.getHTML()

    def _defineSectionMenu(self):
        conferences.WPConferenceDefaultDisplayBase._defineSectionMenu(self)
        self._sectionMenu.setCurrentItem(self._regFormOpt)


class WconfirmEPaymentSixPay(WTemplated):
    def __init__(self, configuration, registrant):
        self._registrant = registrant
        self._conf = configuration

    def getVars(self):
        vars = WTemplated.getVars(self)
        vars["message"] = "Thank you, your payment has been accepted by SixPay"
        vars["trinfo"] = "%s:%s" % (self._registrant.getFirstName(), self._registrant.getSurName())
        return vars


class WPCancelEPaymentSixPay(conferences.WPConferenceDefaultDisplayBase):
    # navigationEntry = navigation.NERegistrationFormDisplay

    def __init__(self, rh, conf, reg):
        conferences.WPConferenceDefaultDisplayBase.__init__(self, rh, conf)
        self._registrant = reg

    def _getBody(self, params):
        wc = WCancelEPaymentSixPay(self._conf, self._registrant)
        return wc.getHTML()

    def _defineSectionMenu(self):
        conferences.WPConferenceDefaultDisplayBase._defineSectionMenu(self)
        self._sectionMenu.setCurrentItem(self._regFormOpt)


class WCancelEPaymentSixPay(WTemplated):
    def __init__(self, conference, reg):
        self._conf = conference
        self._registrant = reg

    def getVars(self):
        vars = WTemplated.getVars(self)
        vars["message"] = "The payment was cancelled (using SixPay)"
        vars["messagedetailPayment"] = "%s:%s" % (self._registrant.getFirstName(), self._registrant.getSurName())
        return vars


class WPNotconfirmEPaymentSixPay(conferences.WPConferenceDefaultDisplayBase):
    # navigationEntry = navigation.NERegistrationFormDisplay

    def __init__(self, rh, conf, reg):
        conferences.WPConferenceDefaultDisplayBase.__init__(self, rh, conf)
        self._registrant = reg

    def _getBody(self, params):
        wc = WNotconfirmEPaymentSixPay(self._conf, self._registrant)
        return wc.getHTML()

    def _defineSectionMenu(self):
        conferences.WPConferenceDefaultDisplayBase._defineSectionMenu(self)
        self._sectionMenu.setCurrentItem(self._regFormOpt)


class WNotconfirmEPaymentSixPay(WTemplated):
    def __init__(self, conference, reg):
        self._conf = conference
        self._registrant = reg

    def getVars(self):
        vars = WTemplated.getVars(self)
        vars["message"] = "You have not confirmed!\n (using SixPay)"
        vars["messagedetailPayment"] = "%s:%s" % (self._registrant.getFirstName(), self._registrant.getSurName())
        return vars
