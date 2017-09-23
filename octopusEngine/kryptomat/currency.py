"""Library for handling operations with cryptocurrencies."""
from __future__ import division, unicode_literals

import json
import logging

import requests

from blockr.api import Api
from fixerio import Fixerio
from octopusEngine.kryptomat.utils import first, parse_utc

BITSTAMP_TICKER_BASE_URL = "https://www.bitstamp.net/api/v2/ticker_hour/{base}{to}/"

logger = logging.getLogger(__name__)

class TransactionException(Exception):
    """Base Exception for Transaction errors."""

    pass


class NotEnoughTransactionConfirmations(TransactionException):
    """Error during validation. Not enough confirmations."""

    confirmations = 0
    wanted = None

    def __init__(self, confirmations, wanted):
        """Get number of confirmations and wanted number."""
        self.confirmations = confirmations
        self.wanted = wanted

    def __str__(self):
        """Convert Exception to str."""
        return "Transaction doesn't have wanted amount of confirmations %d out of %d" % (
            self.confirmations, self.wanted)


class UncomfirmedTransaction(NotEnoughTransactionConfirmations):
    """Error during validation. The transaction is uncomfirmed."""

    def __init__(self):
        """Initialize UncomfirmedTransaction."""
        pass  # override parent __init__

    def __str__(self):
        """Convert Exception to str."""
        return "This transaction is unverified."


class InvalidTransactionValue(TransactionException):
    """The transaction doesn't have wanted amount."""

    value = None
    wanted = None

    def __init__(self, value, wanted):
        """Get obtained value and wanted value."""
        self.value = value
        self.wanted = wanted

    def __str__(self):
        """Convert Exception to str."""
        return "Transaction is for different price wanted %d, but transaction gives only %d" % (
            self.wanted, self.value
        )


class BlockrCurrency(object):
    """API for Blockr.

    parameters:
    * currency       str: Name of currency used.
    * currency_short str: Three letter currency shortcut
    """

    address = None
    api = None
    currency = None
    currency_short = None

    def __init__(self, address):
        """Initialize BlockrCurrency.

        parameters:
        * address str: The default address.
        """
        self.address = address
        self.api = Api(self.currency, use_https=True)

    def _get_my_output(self, transaction, address=None):
        return first((o for o in transaction["trade"]["vouts"]
                      if o["address"] == (address or self.address)), {})

    def get_address(self, address=None):
        """Get information about adress.

        parameters:
        * address str: if specified this address use it instead of self.address
        """
        logger.debug("Obtaining info for address: %s" % self.address)
        return self.api.address(address or self.address)["data"]

    def get_last_transaction(self, since=None, address=None):
        """Get last transaction.

        parameters:
        * since datetime: If specified returns last tx only if it is after this date
        * address str: passes to self.get_address()
        """
        if since is not None:
            logger.debug("Obtaining last tx for address: %s since %s" % (
                address or self.address, since))
        else:
            logger.debug("Obtaining last tx for address: %s" % (address or self.address))
        last_tx = self.get_address(address)["last_tx"]
        if since is None:
            return last_tx
        return last_tx if self.get_time_of_transaction(last_tx) > since else None

    def get_transaction(self, transaction_id):
        """Get transaction out of it's ID.

        parameters:
        * transaction_id str: ID of transaction
        """
        logger.debug("Get info about tx id: %s" % transaction_id)
        return self.api.transaction(transaction_id)["data"]

    def _use_or_get_transaction(self, transaction):
        if type(transaction) == str:
            return self.get_transaction(transaction)
        elif type(transaction) == dict:
            if "trade" in transaction.keys():
                return transaction
            else:
                return self._use_or_get_transaction(transaction["tx"])  # Obtain whole transaction
        else:
            raise TypeError

    def is_transaction_valid(self, transaction, value, confirmations=2):
        """Check if transaction is valid.

        parameters:
        * transaction (transaction dict)|str: transaction dictionary or transaction_id
        * value                        float: Amount we want
        * confirmations                  int: Minimal number of confirmations for
                                              transaction default 2

        Exceptions:
        * NotEnoughTransactionConfirmations - Less than required confirmations
        * InvalidTransactionValue           - Transaction value is lesser
        * UnconfirmedTransaction            - Transaction isn't confirmed yet.
        """
        logger.debug("Check if tx is valid. value: %d confirmations: %d" % (value, confirmations))
        tx = self._use_or_get_transaction(transaction)
        output = self._get_my_output(tx)
        # The amount can be higher e.g. Tip
        if output.get("amount", 0) >= value and \
                tx["confirmations"] >= confirmations and \
                ((tx["is_unconfirmed"] and confirmations == 0) or not tx["is_unconfirmed"]):
            logger.debug("Succes tx is valid.")
            return True
        elif not tx["confirmations"] >= confirmations:
            logger.debug("There is not yet enough confirmations for tx.")
            raise NotEnoughTransactionConfirmations(tx["confirmations"], confirmations)
        elif not output.get("amount", 0) >= value:
            logger.debug("The value is to low. (%f)" % output.get("amount", 0))
            raise InvalidTransactionValue(output.get("amount", 0), value)
        elif tx["is_unconfirmed"]:
            if confirmations == 0:
                return False
            else:
                logger.debug("There is no confirmations yet for tx.")
                raise UncomfirmedTransaction
        else:
            print(output.get("amount", None), value, tx["confirmations"] >= confirmations)

    def get_address_of_author_of_transaction(self, transaction):
        """Get adress of author of transaction.

        parameters:
        * transaction (transaction dict)|str: transaction dictionary or transaction_id
        """
        return self._use_or_get_transaction(transaction)["trade"]["vins"][0]["address"]

    def get_time_of_transaction(self, transaction):
        """Get datetime.datetime of transaction.

        parameters:
        * transaction (transaction dict)|str: transaction dictionary or transaction_id
        """
        return parse_utc(self._use_or_get_transaction(transaction)["time_utc"])

    def get_exchange_rates(self):
        """Get exchange_rate for Class currency."""
        raise DeprecationWarning("Blockr.io exchange rates are unreliable.")
        return self.api.exchange_rate()["data"][0]

    def get_exchange_rate_time(self, exchange_rate=None):
        """Get time of update of exchange_rate.

        parameters:
        * exchange_rate exchange_rate dict: Exchange rate (optional)
        """
        raise DeprecationWarning("Blockr.io exchange rates are unreliable.")
        return parse_utc((exchange_rate or self.get_exchange_rates())["updated_utc"])

    def get_exchange_rate_for_currency(self, currency, exchange_rate=None):
        """Get exchange_rate between Class currency and selected currency.

        parameters:
        * currency                  string: Name of selected currency ("CZK", "USD")
        * exchange_rate exchange_rate dict: Exchange rate (optional)
        """
        raise DeprecationWarning("Blockr.io exchange rates are unreliable.")
        if exchange_rate is None:
            exchange_rate = self.get_exchange_rates()
        return float(exchange_rate["rates"][
            currency.upper() if currency != exchange_rate["base"] else self.currency_short])

    def exchange_currency(self, currency, value, exchange_rate=None):
        """Exchange between Class currency and selected currency.

        Formula:
            value * (1.0 / rate) = x

        parameters:
        * currency                  string: Selected currency
        * value                      float: Number of coins of Class currency
        * exchange_rate exchange_rate dict: Exchange rate (optional)
        """
        raise DeprecationWarning("Blockr.io exchange rates are unreliable.")
        return value * (1.0 / self.get_exchange_rate_for_currency(currency, exchange_rate))


class BitcoinCurrency(BlockrCurrency):
    """Bitcoin currency at Blockr.

    For more see BlockrCurrency class.
    """

    currency = "Bitcoin"
    currency_short = "BTC"


class LitecoinCurrency(BlockrCurrency):
    """Litecoin currency at Blockr.

    For more see BlockrCurrency class.
    """

    currency = "Litecoin"
    currency_short = "LTC"


def convert_currency(base, to, amount):
    """Convert between two cryptocurrencies.

    base     str: code of base currency have to be supported by bitstamp (btc, ltc, xrp).
    to       str: code of currency into which we want to exchange have to be supported by
                  bitstamp (usd, eur) or Europen Bank
    amount float: The amount of money
    """
    logger.debug("Converting currency from %s to %s amount %f" % (base, to, amount))
    assert base.lower() in ["ltc", "btc", "xrp"]

    if base.lower() in ["ltc", "xrp"] and to.lower() == "btc":
        rate = float(json.loads(requests.get(BITSTAMP_TICKER_BASE_URL.format(
                base=base.lower(), to=to.lower())).text)['last'])
    elif to.lower() not in ["usd", "eur"]:  # to currency is not supported by bitstamp
        response = json.loads(requests.get(BITSTAMP_TICKER_BASE_URL.format(
            base=base.lower(), to="usd")).text)
        fixerio = Fixerio(base="USD")  # HAVE TO BE ON SEPERATE LINE
        rate = fixerio.latest()["rates"][to.upper()] * float(response["last"])
    else:
        rate = float(json.loads(requests.get(BITSTAMP_TICKER_BASE_URL.format(
                base=base.lower(), to=to.lower())).text)["last"])

    return amount * rate
