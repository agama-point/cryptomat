import time, datetime
#from datetime import datetime
#from urllib import urlopen
import requests 
import json  

#-----------------------------kurz
#bcfile = urlopen("https://www.bitstamp.net/api/ticker/").read()
def getBTCc():
    jBtc = requests.get("https://www.bitstamp.net/api/ticker/")
    Btcc = jBtc.json()['last']
    return float(Btcc)

def getLTCc():
    jLtc = requests.get("https://www.bitstamp.net/api/v2/ticker/ltcusd/")
    Ltcc = jLtc.json()['last']
    return float(Ltcc)


#---blockchain chain.so/api
def getLastJ(chainJson):
	jsonData = chainJson.json()['data']['txs']
	jsonDataLast = chainJson.json()['data']['txs'][len(jsonData)-1]
	return jsonDataLast
    
def getNumJ(chainJson):
	jsonData = chainJson.json()['data']['txs']
	return len(jsonData)    