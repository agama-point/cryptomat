import argparse
import logging

from octopusEngine.kryptomat import currency
from octopusEngine.wallets import BTC, LTC

parser = argparse.ArgumentParser(
    description='A BTC/LTC Rapsberry Pi automat.'
)
parser.add_argument("-v", "--debug", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-t", "--test",
                    help="Print current rates of LTC/BTC and show last tx of wallets.",
                    action="store_true")
parser.add_argument("-qr", "--qr-code-output-path",
                    help="The path where to generate QR code. Default: qrcode.png",
                    default="qrcode.png")


logger = logging.getLogger(__name__)

def main():
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('Debug mode enabled.')
    # ###### REAL CODE STARTS HERE !! ######

    print("IT WORKS!!")
    print("QR code output path is %s" % args.qr_code_output_path)

    if args.test:
        print("1 BTC:")
        print("* USD: %f $" % currency.convert_currency("BTC", "USD", 1))
        print("* CZK: %f Kc" % currency.convert_currency("BTC", "CZK", 1))
        print("1 LTC:")
        print("* USD: %f $" % currency.convert_currency("LTC", "USD", 1))
        print("* CZK: %f Kc" % currency.convert_currency("LTC", "CZK", 1))

        print("Last tx in BTC wallet %s:" % BTC)
        btc_curr = currency.BitcoinCurrency(address=BTC)
        print(btc_curr.get_last_transaction())

        print("Last tx in LTC wallet %s:" % BTC)
        ltc_curr = currency.LitecoinCurrency(address=LTC)
        print(ltc_curr.get_last_transaction())
