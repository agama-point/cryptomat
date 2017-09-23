from __future__ import print_function

import argparse
import logging
import os
import sys
import time
from builtins import input

from PIL import Image

from octopusEngine.kryptomat.currency import (BitcoinCurrency,
                                              InvalidTransactionValue,
                                              LitecoinCurrency,
                                              NotEnoughTransactionConfirmations,
                                              UncomfirmedTransaction,
                                              convert_currency)
from octopusEngine.wallets import BTC, LTC

parser = argparse.ArgumentParser(
    description='A test script for octopusEngine.kryptomat.currency lib'
)
parser.add_argument("-v", "--debug", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-qr", "--qr-code-output-path",
                    help="The path where to generate QR code. Default: qrcode.png",
                    default="qrcode.png")

logger = logging.getLogger(__name__)


def emulator(args=None):
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('Debug mode enabled.')

    curr = input("What currency do you want to use? (BTC, LTC): ")
    if curr not in ["BTC", "LTC"]:
        print("Invalid currency")
        sys.exit(1)

    if curr == "BTC":
        curr_obj = BitcoinCurrency(address=BTC)
    if curr == "LTC":
        curr_obj = LitecoinCurrency(address=LTC)

    amount = float(input("Enter the amount in %s: " % curr))
    print("Obtaining convert rates...")
    print("USD: %f $" % convert_currency(curr, "USD", amount))
    print("CZK: %f Kc" % convert_currency(curr, "CZK", amount))
    if curr == "BTC":
        qrGet = "bitcoin:" + curr_obj.address + "?amount=" + str(amount)
    if curr == "LTC":
        qrGet = "litecoin:" + curr_obj.address + "?amount=" + str(amount)

    os.system('qrencode -o %s ' % args.qr_code_output_path + qrGet)
    img = Image.open(args.qr_code_output_path)
    img.show(title="QR Payment")

    print("Waiting for payment 30s.")
    time.sleep(30)

    while True:
        trans = curr_obj.get_last_transaction()
        try:
            out = curr_obj.is_transaction_valid(trans, amount)
            if out:
                print("Payment recieved from %s" % (
                    curr_obj.get_address_of_author_of_transaction(trans)))
                break
        except UncomfirmedTransaction:
            print("ERR: transaction is not yet confirmed!")
        except NotEnoughTransactionConfirmations:
            print("ERR: The transaction haven't get yet enough confirmations. "
                  "Have %d out of 2" % (trans["confirmations"]))
        except InvalidTransactionValue as e:
            print(str(e))
        except AttributeError as e:
            if trans is None:
                print("ERR: No transactions yet.")
            else:
                raise e
        print("Sleeping 10s for another check.")
        time.sleep(10)

if __name__ == "__main__":
    emulator()
