import time, datetime
#from datetime import datetime
#from urllib import urlopen
import requests 
import json

class oeCrypto5():
  def __init__(self,coin,wallAdr):
      self.coin = coin
      self.wallAdr = wallAdr
    
  def setCoin(self,coin):     self.coin = coin
  def getCoin(self):     return self.coin
  def getAdr(self):     return self.wallAdr
  
  def getCourse(self):
      if (self.coin=="BTC"):
        jBtc = requests.get("https://www.bitstamp.net/api/ticker/")
        Xtcc = jBtc.json()['last']
      if (self.coin=="LTC"):
        jLtc = requests.get("https://www.bitstamp.net/api/v2/ticker/ltcusd/")
        Xtcc = jLtc.json()['last']     
      return Xtcc  
  
  def getTxJson(self):
      if (self.coin=="BTC"):
        resourceBTC = "https://chain.so/api/v2/get_tx_received/BTC/"+self.wallAdr
        self.j = requests.get(resourceBTC)
      if (self.coin=="LTC"):
        resourceBTC = "https://chain.so/api/v2/get_tx_received/LTC/"+self.wallAdr
        self.j = requests.get(resourceBTC)     
      return self.j
    
  def getTxJsonLast(self):
      """
     [0] jsonLast
     [1] len
     [2] value
     [3] timeUx
     [4] time str
      """    
      
      if (self.coin=="BTC"):
         resource = "https://chain.so/api/v2/get_tx_received/BTC/"+self.wallAdr
         j = requests.get(resource)
      
      if (self.coin=="LTC"):
         resource = "https://chain.so/api/v2/get_tx_received/LTC/"+self.wallAdr
         j = requests.get(resource)
        
      jsonData = j.json()['data']['txs']
      jsonDataLast = j.json()['data']['txs'][-1] #[len(jsonData)-1]
      lastTransTime = datetime.datetime.fromtimestamp(int(jsonDataLast['time'])).strftime('%Y-%m-%d %H:%M:%S')
      #lastTransTime = jsonDataLast['time']
      return jsonDataLast, len(jsonData), jsonDataLast['value'],jsonDataLast['time'],lastTransTime  ##,lastTransTime # jsonLast + number of tx   


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