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
from __future__ import absolute_import, division
from MaKaC.epayment import BaseEPayMod, BaseTransaction
from MaKaC.webinterface import urlHandlers


from .webinterface import urlHandlers as localUrlHandlers
from . import MODULE_ID, six_logger
import md5


class SixPayMod(BaseEPayMod):
    """Payment Module for SIX Payment Service"""
    def __init__(self, data=None):
        six_logger.info('%s', data)
        BaseEPayMod.__init__(self)
        self._title = "SixPay"
        # self._url = "https://yellowpay.postfinance.ch/checkout/Yellowpay.aspx?userctrl=Invisible"
        self._url = "https://www.saferpay.com/hosting"
        self._shopID = ""
        self._masterShopID = ""
        self._hashSeed = ""
        if data is not None:
            self.setValues(data)

    def getId(self):
        return MODULE_ID

    def clone(self, newSessions):
        self_clone = SixPayMod()
        self_clone.setTitle(self.getTitle())
        self_clone.setUrl(self.getUrl())
        self_clone.setShopID(self.getShopID())
        self_clone.setMasterShopID(self.getMasterShopID())
        self_clone.setHashSeed(self.getHashSeed())
        self_clone.setEnabled(self.isEnabled())
        return self_clone

    def setValues(self, data):
        self.setTitle(data.get("title", "epayment"))
        self.setUrl(data.get("url", ""))
        self.setShopID(data.get("shopid", ""))
        self.setMasterShopID(data.get("mastershopid", ""))
        self.setHashSeed(data.get("hashseed", ""))

    def getUrl(self):
        return self._url

    def setUrl(self, url):
        self._url = url

    def getShopID(self):
        return self._shopID

    def setShopID(self, shopID):
        self._shopID = shopID

    def getMasterShopID(self):
        return self._masterShopID

    def setMasterShopID(self, masterShopID):
        self._masterShopID = masterShopID

    def getHashSeed(self):
        return self._hashSeed

    def setHashSeed(self, hashSeed):
        self._hashSeed = hashSeed

    def getFormHTML(self, prix, Currency, conf, registrant, lang="en_GB", secure=False):
        six_logger.info('%s', (prix, Currency, conf, registrant, "en_GB", False))
        l=[]
        l.append("%s=%s"%("confId",conf.getId()))
        l.append("%s=%s"%("registrantId",registrant.getId()))
        param= "&".join( l )
        m = md5.new()
        m.update(self.getShopID())
        m.update(Currency)
        m.update("%.2f" % prix)
        m.update(self.getHashSeed())
        txtHash = m.hexdigest()
        s = """ <form action="%s" method="POST" id="%s">
                      <input type="hidden" name="txtShopId" value="%s">
                      <input type="hidden" name="txtLangVersion" value="%s">
                      <input type="hidden" name="txtOrderTotal" value="%s">
                      <input type="hidden" name="txtArtCurrency" value="%s">
                      <input type="hidden" name="txtHash" value="%s">
                      <input type="hidden" name="txtShopPara" value="%s">
                   </form>
                       """ % (
            self.getUrl(),
            self.getId(),
            self.getMasterShopID(),
            "2057",
            prix,
            Currency,
            txtHash,
            param
        )
        return s

    def getConfModifEPaymentURL(self, conf):
        six_logger.info('%s', conf)
        return localUrlHandlers.UHConfModifEPaymentSixPay.getURL(conf)


class TransactionSixPay(BaseTransaction):
    """Transaction for SIX Payment Service"""
    def __init__(self, parms):
        six_logger.info('%s', parms)
        BaseTransaction.__init__(self)
        self._Data = parms

    def getId(self):
        try:
            return self._id
        except AttributeError:
            self._id = "sixpay"
            return self._id

    def getTransactionHTML(self):
        textOption = """\
                          <tr>
                            <td align="right"><b>ESR Member:</b></td>
                            <td align="left">%s</td>
                          </tr>
                          <tr>
                            <td align="right"><b>ESR Ref:</b></td>
                            <td align="left">%s</td>
                          </tr>
         """ % (self._Data["ESR_Member"], self._Data["ESR_Ref"])
        return """\
                        <table>
                          <tr>
                            <td align="right"><b>Payment with:</b></td>
                            <td align="left">SixPay</td>
                          </tr>
                          <tr>
                            <td align="right"><b>Payment Date:</b></td>
                            <td align="left">%s</td>
                          </tr>
                          <tr>
                            <td align="right"><b>TransactionID:</b></td>
                            <td align="left">%s</td>
                          </tr>
                          <tr>
                            <td align="right"><b>Order Total:</b></td>
                            <td align="left">%s %s</td>
                          </tr>
                          <tr>
                            <td align="right"><b>PayMet:</b></td>
                            <td align="left">%s</td>
                          </tr>
                          %s
                        </table>""" % (
            self._Data["payment_date"],
            self._Data["TransactionID"],
            self._Data["OrderTotal"],
            self._Data["Currency"],
            self._Data["PayMet"],
            textOption
        )

    def getTransactionTxt(self):
        textOption = """
\tESR Member:%s\n
\tESR Ref:%s\n
""" % (self._Data["ESR_Member"], self._Data["ESR_Ref"])
        return """
\tPayment with:SixPay\n
\tPayment Date:%s\n
\tTransactionID:%s\n
\tOrder Total:%s %s\n
\tPayMet:%s
%s
""" % (
            self._Data["payment_date"],
            self._Data["TransactionID"],
            self._Data["OrderTotal"],
            self._Data["Currency"],
            self._Data["PayMet"],
            textOption)


def getPayMod():
    return SixPayMod()


def getPayModClass():
    return SixPayMod
