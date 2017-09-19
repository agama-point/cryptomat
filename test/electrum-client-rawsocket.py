#!/usr/bin/env python3

##http://explorer.litecoin.net/chain/Litecoin/q/getreceivedbyaddress/LNTKxPMWDNAHT1rUkAGmS81CMBHqB3W723
##chain.so
##https://chain.so/api/v2/get_tx_received/LTC/LNTKxPMWDNAHT1rUkAGmS81CMBHqB3W723

#from bip32utils import BIP32Key
from pycoin.tx import Tx
import socket
import json
import time


def get_from_electrum(s, method, params=[]):
    params = [params] if type(params) is not list else params
    s.send(json.dumps({"id": 0, "method": method, "params": params}).encode() + b'\n')
    time.sleep(1);
    return json.loads(s.recv(999999)[:-1].decode())


def get_balance(s, addr):
    res = get_from_electrum(s, "blockchain.address.get_balance", addr)
    return res['result']['confirmed']/100000000


def get_txs(s, addr):
    res = get_from_electrum(s, "blockchain.address.get_history", [addr])
    return res['result']


def get_tx(s, tx):
    res = get_from_electrum(s, "blockchain.transaction.get", tx)
    return res['result']


def get_block(s, height):
    res = get_from_electrum(s, "blockchain.block.get_header", height)
    return res['result']

testPubkey = "xpub6CfjpRozdbCe8qkGxQoFMoeiHqtexbfWS71xtPU3gMhH5zXscuzZqBqjQ44f59bhUtpCVM2dEBJEysjPQWBQf1b21ii1fNKHfGcyczUzgp6"
prodLiteKey = "LM4qTR7WZiUe7BAxesj4N1UPadWAnQEj92"

##a = BIP32Key.fromExtendedKey(testPubkey)
##a = a.ChildKey(0).ChildKey(0)

# Bitcoin Core Mainnet
electrum_socket = socket.create_connection(('petrkr.net', 50001))

# Bitcoin Core Testnet
electrum_socket_testnet = socket.create_connection(('bohol.petrkr.net', 51001))

# Litecoin Mainnet
electrum_socket_litecoin = socket.create_connection(('bohol.petrkr.net', 60001))

txs = get_txs(electrum_socket_litecoin, prodLiteKey)
tx_raw = get_tx(electrum_socket_litecoin, txs[0]['tx_hash'])
tx_block = get_block(electrum_socket_litecoin, txs[0]['height'])

tx = Tx.Tx.from_hex(tx_raw)

print(tx_block)

print(tx)

##print("%s (%s BTC) - %s" % (a.Address(), get_balance(electrum_socket, a.Address()), "N/A" if a.public else a.WalletImportFormat()))
print("%s (%s LTC)" % (prodLiteKey, get_balance(electrum_socket_litecoin, prodLiteKey)))
