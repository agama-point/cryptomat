# ------------------------------
# 2017/09 - RPi3 (wifi) + Python3
# /dev/ttyAMA0 previously used to access the UART now connects to Bluetooth.
# The miniUART is now available on /dev/ttyS0.
#
#n ext-write-test3 > next-read-test3
#
ver="2017/09"

from myWallets import  getWBTC, getWLTC
wallAdrBTC=getWBTC()
wallAdrLTC=getWLTC()

#from urllib import urlopen
import requests 
import json 

from octopusEngineLib.oeUtil import *
from octopusEngineLib.oeCrypto import *

from octopusEngineLib.oeHW3 import *
import sys, os, subprocess, time, datetime

#mport urllib2 #course
#import json
#from socket import gethostname, gethostbyname #getIp
from time import sleep

from socket import gethostname, gethostbyname #getIp
from time import sleep

netOk = True #wifi test - todo
debugPrint = True
testMode = False
seleC = "?" #BTC/LTC
CZKUSD = 22.5

neXcmd("page intro")
pip(1800,0.05)
neXcmd("page intro")

i=0
numi = 3
while i<numi:
  print(i)	
  neXtxt("t0",str(numi-i))
  i +=1
  time.sleep(1)
neXtxt("t0"," ")  
#---------------------init---------------
from threading import Thread, Event
nexThread = True #running

def nexth(): ##thread
 global nxRead, nexThread
 s.flushInput()
 cntx=0
 nacti= 7 #ok
 while nexThread:     
   try:
    hodnota = s.read(nacti) #7
    #print(hodnota),
    nxRead = hodnota[2:3]
    print(nxRead)   
   except:
    # print "Err.data"
    nic = True   
   
   time.sleep(0.7)  #0.7)
   cntx=cntx+1

# thread for reading
thrnx = Thread(target=nexth)
thrnx.start()

if (debugPrint):
   print(">>> octopusengine.org/api --- getServerTime()")	
   print(getServerTime())
   print("")
      
nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#addLog("T-"+nowTim+" | "+str(deltaMin)+ " min. | val:"+str(transValue)+" s")	 
#addLog("> K:"+str(lastNum)+", $"+str(valUSD)+", a:"+str(amountS)+" s")
addLog("T-"+nowTim+"*")

#---------------------start---------------
#---bitstamp BTC/USD LTC/USD
Btcc = getBTCc()
neXtxt("t0",str(Btcc)+" B/$ ") 
time.sleep(1)
Ltcc = getLTCc()
neXtxt("t0",str(Ltcc)+" L/$ ") 
time.sleep(2)

if (debugPrint):
   if (debugPrint): print(">>> bitstamp.net/api/ticker ---")	
   print("BTC:"+str(Btcc))
   print("LTC:"+str(Ltcc))   


if (testMode):
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
  print("last > from " + str(getNumJ(j)))
  print(datetime.datetime.fromtimestamp(int(jsonDataLast['time'])).strftime('%Y-%m-%d %H:%M:%S'))
  #print(j.json()['data']['txs'][arrayCnt-1]['value'])     
  print(jsonDataLast['value']) 
  time.sleep(2)

  #------------LTC--------------------------  
  resourceLTC = "https://chain.so/api/v2/get_tx_received/LTC/"+wallAdrLTC  
  j = requests.get(resourceLTC) 
  lastTransTime = datetime.datetime.fromtimestamp(int(getLastJ(j)['time'])).strftime('%Y-%m-%d %H:%M:%S')
  lastTransValue = getLastJ(j)['value']
  print("--- litecoin last transaction ---")
  print("last > from " + str(getNumJ(j)))
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


#----------------------select > read ---------------
neXcmd("page select")
neXtxt("ts1","::")
neXtxt("ts2","BTC/USD")
neXtxt("ts3",str(Btcc))
neXtxt("ts4","-")
neXtxt("ts5","LTC/USD")
neXtxt("ts6",str(Ltcc))
neXtxt("ts7","-")

cekej = True
ccnt=0
#s2.flushInput()
#for rx in range (20):

while cekej: #cekani na stisk
     ccnt=ccnt+1
     ctu = nxRead
     #neXtxt("d0",str(ccnt) + ">"+str(ctu))
     neXtxt("d0",str(ccnt))
     #if (ctu!="00"): 
     ###pip(1800,0.05) #ctu
     #print("---stisknuto-ok---" + ctu)
     if (ctu==nx1):
         pip(1800,0.05)
         print("---nx1")
         valUSD= 1.0
         cekej = False
     if (ctu==nx2):
         pip(1800,0.05)
         print("---nx2")
         valUSD= 2.0
         cekej = False
     if (ctu==nx3):
         pip(1800,0.05)
         print("---nx3")
         valUSD= 3.0
         cekej = False
     if (ctu==nx4):
         pip(1800,0.05)
         print("---nx4")
         valUSD= 5.0
         cekej = False      
     if (ctu==nx5):
         pip(1800,0.05)
         print("---nx5")
         valUSD= 8.0
         cekej = False
     if (ctu==nx6):
         pip(1800,0.05)
         print("---nx6")
         valUSD= 10.0
         cekej = False         
         
         
     #else: 
     #   print("---nic----" + ctu)
     #   nic = True
     time.sleep(0.7)
 
time.sleep(2)

neXcmd("page selecoin")
ctu = ""
cekej2 = True
ccnt=0
while cekej2: #cekani na stisk
     ccnt=ccnt+1
     ctu = nxRead
     #neXtxt("d0",str(ccnt) + ">"+str(ctu))
     #neXtxt("d0",str(ccnt))    
     ###pip(1800,0.05) #ctu    
     if (ctu==nxBTC):
         pip(1800,0.05)
         seleC="BTC"
         cekej2 = False
     if (ctu==nxLTC):
         pip(1800,0.05)
         seleC="LTC"
         cekej2 = False
     #if (ctu==nx3):
     #    print("nx3")
     #    cekej = False 
     
     time.sleep(0.7)
print("selected currency: "+seleC)     
#-----------------------qr----------------------     
#if isJmp1(): text="off-line"    
#else: text="on-line"  
#neXtxt("d0",text)

neXcmd("page qr")
neXcmd("page qr")
#am =0.0112233
##valUSD=1

if(seleC=="BTC"):
  neXtxt("t1","Bitcoin")   
  amount=round(float(valUSD/Btcc),8)
  amountS=amount*100000000
  #print ">>>>>>>>>>", valUSD, lastNum, amount, amountS  
  text="$"+str(Btcc)    
  neXtxt("t2",text) 
  kuryCz = Ltcc*CZKUSD
  text="("+str(kuryCz) +" Kc)"   
  neXtxt("t3",text) 
  time.sleep(0.2)
  neXtxt("t8",wallAdrBTC[:7]+"..."+wallAdrBTC[-7:])
  #
  
if(seleC=="LTC"):
  neXtxt("t1","Litecoin")  
  amount=round(float(valUSD/Ltcc),8)
  amountS=amount*100000000
  #print ">>>>>>>>>>", valUSD, lastNum, amount, amountS  
  text="$"+str(Ltcc)    
  neXtxt("t2",text) 
  kuryCz = Ltcc*CZKUSD
  text="("+str(kuryCz) +" Kc)"   
  neXtxt("t3",text) 
  time.sleep(0.2)
  neXtxt("t8",wallAdrLTC[:7]+"..."+wallAdrLTC[-7:])
  
neXtxt("t10","TO PAY:")   
neXtxt("t0",seleC)   
text="$"+str(valUSD)   
neXtxt("t4",text) 
text=str(amount)+" "+seleC   
neXtxt("t5",text) 
text="> "+str(valUSD*CZKUSD)+" Kc"    
neXtxt("t6",text)
time.sleep(0.2) 


am =0.0112233
displayQR(True,"litecoin:"+wallAdrLTC+"?amount="+str(am))


cntWait=0
cntWait2=0
while (not isJmp1()):
      time.sleep(0.3)
      neXtxt("d0","PAY")  
      time.sleep(0.3)
      neXtxt("d0","   ")
      if (cntWait2%2): 
         neXtxt("t9","than press BUTTON")
      else:       
         neXtxt("t9","sann QR & pay") 
      if (cntWait%2): 
        cntWait2 = cntWait2+1   
      cntWait = cntWait+1 

#pip(1800,0.05)
pip1()   
time.sleep(1) 
neXcmd("page blockch") 
neXcmd("page blockch")
time.sleep(0.3) 
if True:  
  if netOk: neXtxt("tb9"," ")
  else: neXtxt("tb9","sorry - off Line or net.Err")  
  
  neXtxt("tb0","Last transaction info:")
  if(seleC=="LTC"):
    neXtxt("tb1","> $"+str(valUSD)+" | "+str(Ltcc)+" USD/LTC" )
    txAmount =  "amount: "+str(amount) + "LTC"
  if(seleC=="BTC"):
    neXtxt("tb1","> $"+str(valUSD)+" | "+str(Btcc)+" USD/BTC" )
    txAmount =  "amount: "+str(amount) + "BTC"
  
  
  #txAmount =  "amount: "+str(amountS) + " Satoshi"
   
  time.sleep(0.5)
  #nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  dtServer = datetime.datetime.strptime(getServerTime(), '%Y-%m-%d %H:%M:%S')
  #dtServerS = dtServer[-8:]
  dtDevice = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  
  
  #timDelta= int(nowTime)-int(txsTime) 
  
  
  neXtxt("tb2",txAmount)
  neXtxt("tb3","serverTime: "+str(dtServer)[-8:]) 
  neXtxt("tb4","deviceTime:  "+str(dtDevice)[-8:])
  time.sleep(0.5)
  neXtxt("tb5","Blockchain info testing | "+ver) 
  neXtxt("tb6","server: "+str(dtServer)) 
  neXtxt("tb7","device:  "+str(dtDevice)) 
  neXtxt("tb8"," ") 
  
  ##neXtxt("tb9","transactionT "+transTime) 
#-------------------------end --------------
