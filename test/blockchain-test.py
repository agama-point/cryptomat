# ------------------------------
# 2017/09 - RPi3 (wifi)
# /dev/ttyAMA0 previously used to access# https://github.com/octopusengine/simpleBitcoinMachine
#
# ing.Jan Copak - Czechrepublic / Prague
# octopusengine.eu | newreality.eu
#--------------------------------------------
#
#--------------------------------------------
#https://github.com/blockchain/receive-payments-demos/blob/master/python/receive_demo/views.py
#2017/08> https://chain.so/api/v2/get_tx_received/LTC/LNTKxPMWDNAHT1rUkAGmS81CMBHqB3W723
#--------------------------------------------
import time, datetime
#from datetime import datetime
from urllib import urlopen
import requests 
import json    
#my wallet address:
from myWallets import  getWBTC, getWLTC
wallAdrBTC=getWBTC()
wallAdrLTC=getWLTC()

debugPrint = True

#---blockchain chain.so/api
def getLast(chainJson):
	jsonData = chainJson.json()['data']['txs']
	jsonDataLast = chainJson.json()['data']['txs'][len(jsonData)-1]
	return jsonDataLast


#---server time--- (start > RPi was off-line)
def getServerTime():
   serverTime = urlopen("http://www.octopusengine.eu/api/datetime.php").read()
   return str(serverTime) 
    
   
if (debugPrint):
   print(">>> octopusengine.org/api --- getServerTime()")	
   print(getServerTime())
   print("")

#---bitstamp BTC/USD LTC/USD

#bcfile = urlopen("https://www.bitstamp.net/api/ticker/").read()
jBtc = requests.get("https://www.bitstamp.net/api/ticker/")
Btcc = jBtc.json()['last']
time.sleep(1)

jLtc = requests.get("https://www.bitstamp.net/api/v2/ticker/ltcusd/")
Ltcc = jLtc.json()['last']
time.sleep(2)

if (debugPrint):
   if (debugPrint): print(">>> bitstamp.net/api/ticker ---")	
   print("BTC:"+str(Btcc))
   print("LTC:"+str(Ltcc))

   print(">>> bitcoin last transaction ---")

#------------BTC-------------------------- 
resourceBTC = "https://chain.so/api/v2/get_tx_received/BTC/"+wallAdrBTC
j = requests.get(resourceBTC)
#print(j.json()['data']['txs'])  
#arrayCnt = len(j.json()['data']['txs'])
jsonData = j.json()['data']['txs']
jsonDataLast = j.json()['data']['txs'][len(jsonData)-1]

#print(j.json()['data']['txs'][0]['time']) 
#print(j.json()['data']['txs'][arrayCnt-1]['time'])  
print("last > from " + str(len(jsonData)))
print(datetime.datetime.fromtimestamp(int(jsonDataLast['time'])).strftime('%Y-%m-%d %H:%M:%S'))
#print(j.json()['data']['txs'][arrayCnt-1]['value'])     
print(jsonDataLast['value']) 
time.sleep(2)

#------------LTC--------------------------  
resourceLTC = "https://chain.so/api/v2/get_tx_received/LTC/"+wallAdrLTC  
j = requests.get(resourceLTC)
lastTransTime = datetime.datetime.fromtimestamp(int(getLast(j)['time'])).strftime('%Y-%m-%d %H:%M:%S')
lastTransValue = getLast(j)['value']
print("--- litecoin last transaction ---")
print("last > from " + str(len(jsonData)))
print(lastTransTime)   
print(lastTransValue) 

dtTrans = datetime.datetime.strptime(lastTransTime, '%Y-%m-%d %H:%M:%S')
dtTransUx = time.mktime(dtTrans.timetuple())
dtServer = datetime.datetime.strptime(getServerTime(), '%Y-%m-%d %H:%M:%S')
dtServerUx = time.mktime(dtServer.timetuple())
dtUx = dtServerUx-dtTransUx 

print("")
print("--- dateTime transaction ---")
print(str(dtTrans) +" / "+ str(dtTransUx)) 
print(str(dtServer) +" / "+ str(dtServerUx))
 
print(str(dtServer-dtTrans) + " / "+str(dtUx)+ " /m/ "+str(int(dtUx/60))+ " /h/ "+str(int(dtUx/3600))) 

time.sleep(2)
  
#---/end 

 
