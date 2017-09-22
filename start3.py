#!/usr/bin/python3
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

cB=oeCrypto5("BTC",wallAdrBTC) #Bitcoin setup
cL=oeCrypto5("LTC",wallAdrLTC) #Litecoin setup
#cD=oeCrypto5("DSH",wallAdrDSH)

netOk = True #wifi test - todo
slowZeroW = False
debugPrint = True
testMode = False
seleC = "?" #BTC/LTC
CZKUSD = 22.5
seleC="???"

#---------------------init---------------
from threading import Thread, Event
nexThread = True #running

def nextionThread(): ##thread
   global nxRead, nexThread
   s.flushInput()
   cntx=0
   readBytes= 7 #ok
   while nexThread:     
     try:
         hodnota = s.read(readBytes) #7
         #print(hodnota),
         nxRead = hodnota[2:3]
         print(nxRead)   
     except:
         # print "Err.data"
         nic = True   
   
     time.sleep(0.69)  #0.7)
     cntx=cntx+1

if __name__ == "__main__":
    # thread for reading
    thrNx = Thread(target=nextionThread)
    thrNx.daemon = True
    thrNx.start()


#-------- fce
def oneValidation():
    """
    [0] jsonLast
    [1] len
    [2] value
    [3] timeUx
    [4] time str
    """
    if(seleC=="LTC"):
        arrDataLast = cL.getTxJsonLast()      
    if(seleC=="BTC"):
        arrDataLast = cB.getTxJsonLast()
    #print("selected: "+ seleC)    
    print("last > from "+str(arrDataLast[1])) 
    lastTransTime = arrDataLast[4]
    lastTransValue = arrDataLast[2]
    print("[time]"+lastTransTime)
    print("[value]"+lastTransValue)

    #UTC x local time

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
    
    deltaMin = round((float(dtUx/60)),2)-120 #todo pekr #timezone
    deltaMin = int(deltaMin*100)/100
  
    neXtxt("tb6","T:"+str(dtTrans) +" / "+ str(dtTransUx))
    neXtxt("tb7","S:"+str(dtServer) +" / "+ str(dtServerUx))
    #neXtxt("tb8",str(dtServer-dtTrans) + "/"+str(dtUx)+ " m:"+str(int(dtUx/60))+ " h:"+str(int(dtUx/3600)))
    neXtxt("tb8","Last.tx min."+str(deltaMin)+ " val:"+str(lastTransValue))

    return deltaMin

#---------------------start---------------
def oneLoop():
 global seleC
 print("------------------------one Loop")
 neXcmd("page intro")
 pip1()
 neXcmd("page intro")
 i=0
 numi = 6
 while i<numi:
      print(i)
      neXtxt("t0",str(numi-i))
      i +=1
      time.sleep(1)
 neXtxt("t0"," ")
 time.sleep(3)
 
 neXcmd("page select")
 pip1()
 neXcmd("page select")
 time.sleep(1)
 
 neXtxt("ts1","::")
 neXtxt("ts2","BTC/USD")
 neXtxt("ts3","???")
 neXtxt("ts4","-")
 neXtxt("ts5","LTC/USD")
 neXtxt("ts6","???")
 neXtxt("ts7","-")
 time.sleep(1) 
      
 nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 #addLog("T-"+nowTim+" | "+str(deltaMin)+ " min. | val:"+str(transValue)+" s")	 
 #addLog("> K:"+str(lastNum)+", $"+str(valUSD)+", a:"+str(amountS)+" s")
 addLog("T-"+nowTim+"*")
 
 if (debugPrint):
     print(">>> octopusengine.org/api --- getServerTime()")	
     print(getServerTime())
     print("")

 #---bitstamp BTC/USD LTC/USD
 Btcc = getBTCc()
 #neXtxt("t0",str(Btcc)+" B/$ ") 
 time.sleep(0.3)
 Ltcc = getLTCc()
 #neXtxt("t0",str(Ltcc)+" L/$ ")
 time.sleep(0.1)
 
 neXtxt("ts1","::")
 neXtxt("ts2","BTC/USD")
 neXtxt("ts3",str(Btcc))
 neXtxt("ts4","-")
 neXtxt("ts5","LTC/USD")
 neXtxt("ts6",str(Ltcc))
 neXtxt("ts7","-")
 time.sleep(1)

 if (debugPrint):
     if (debugPrint): print(">>> bitstamp.net/api/ticker ---")	
     print("BTC:"+str(Btcc))
     print("LTC:"+str(Ltcc))

 if (testMode):
  print("-----------test mode: -------------")  
  print(">>>  last transaction ---"+cB.getCoin())
  print("adr: "+cB.getAdr())
  print(str(cB.getCourse()))
  #jsonDataLast=cB.getTxJsonLast()[0]
  arrDataLast = cB.getTxJsonLast()
  
  #print("last > from "+str(cB.getTxJsonLast()[1]))
  print("last > from "+str(arrDataLast[1]))  
  
  #lastTransTime = datetime.datetime.fromtimestamp(int(arrDataLast[3])).strftime('%Y-%m-%d %H:%M:%S')
  lastTransTime = arrDataLast[4]
  #lastTransValue = jsonDataLast['value']
  lastTransValue = arrDataLast[2]
  print("[time]"+lastTransTime)   
  print("[value]"+lastTransValue)
  
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
  
  print("------------------------")
  print(">>>  last transaction ---"+cL.getCoin())
  print("adr: "+cL.getAdr())
  print(str(cL.getCourse()))
  print("---")
  arrDataLast = cL.getTxJsonLast()
  #jsonDataLast=arrDataLast[0]
    
  print("last > from "+str(arrDataLast[1]))  
  lastTransTime = arrDataLast[4]
  lastTransValue = arrDataLast[2]
  print("[time]"+lastTransTime)   
  print("[value]"+lastTransValue)

  dtTrans = datetime.datetime.strptime(lastTransTime, '%Y-%m-%d %H:%M:%S')
  dtTransUx = arrDataLast[3] #time.mktime(dtTrans.timetuple())
  dtServer = datetime.datetime.strptime(getServerTime(), '%Y-%m-%d %H:%M:%S')
  dtServerUx = time.mktime(dtServer.timetuple())
  dtUx = dtServerUx-dtTransUx 

  print("")
  print("--- dateTime transaction ---")
  print(str(dtTrans) +" / "+ str(dtTransUx)) 
  print(str(dtServer) +" / "+ str(dtServerUx))
 
  print(str(dtServer-dtTrans) + " / "+str(dtUx)+ " /m/ "+str(int(dtUx/60))+ " /h/ "+str(int(dtUx/3600))) 

 #----------------------select > read ---------------
 waitNx = True
 ccnt=0
 #s2.flushInput()
 #for rx in range (20):

 while waitNx: #cekani na stisk
     ccnt=ccnt+1
     ctu = nxRead
     ##neXtxt("d0",str(ccnt) + ">"+str(ctu))
     #if (ctu!="00"): 
     ###pip(1800,0.05) #ctu
     #print("---stisknuto-ok---" + ctu)
     if (ctu==nx1):
         pip(1800,0.05)
         print("---nx1")
         valUSD= 1.0
         waitNx = False
     if (ctu==nx2):
         pip(1800,0.05)
         print("---nx2")
         valUSD= 2.0
         waitNx = False
     if (ctu==nx3):
         pip(1800,0.05)
         print("---nx3")
         valUSD= 3.0
         waitNx = False
     if (ctu==nx4):
         pip(1800,0.05)
         print("---nx4")
         valUSD= 5.0
         waitNx = False      
     if (ctu==nx5):
         pip(1800,0.05)
         print("---nx5")
         valUSD= 8.0
         cekej = False
     if (ctu==nx6):
         pip(1800,0.05)
         print("---nx6")
         valUSD= 10.0
         waitNx = False         
         
         
     #else: 
     #   print("---nic----" + ctu)
     #   nic = True
     time.sleep(0.6)
 
 time.sleep(2)
 
 neXcmd("page selecoin")
 pip1()
 neXcmd("page selecoin")
 ctu = ""
 waitNx2 = True
 ccnt=0
 while waitNx2: #cekani na stisk
     ccnt=ccnt+1
     ctu = nxRead
     #neXtxt("d0",str(ccnt) + ">"+str(ctu))
     #neXtxt("d0",str(ccnt))    
     ###pip(1800,0.05) #ctu    
     if (ctu==nxBTC):
         pip(1800,0.05)
         seleC="BTC"
         waitNx2 = False
     if (ctu==nxLTC):
         pip(1800,0.05)
         seleC="LTC"
         waitNx2 = False
     #if (ctu==nx3):
     #    print("nx3")
     #    cekej = False 
     
     time.sleep(0.57)
 print("selected currency: "+seleC)     
 #-----------------------qr----------------------     
 # if isJmp1(): text="off-line"    
 #else: text="on-line"  
 #neXtxt("d0",text)

 neXcmd("page qr")
 pip1()
 neXcmd("page qr")
 #am =0.0112233
 ##valUSD=1

 neXtxt("t10","TO PAY:")   
 neXtxt("t0",seleC)   
 text="$"+str(valUSD)   
 neXtxt("t4",text)
 text="> "+str(valUSD*CZKUSD)+" Kc"    
 neXtxt("t6",text)
 time.sleep(1)   

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
  text=str(amount)+" "+seleC   
  neXtxt("t5",text) 
  neXtxt("t8",wallAdrBTC[:7]+"..."+wallAdrBTC[-7:])
  displayQR(slowZeroW,"bitecoin:"+wallAdrBTC+"?amount="+str(amount))
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
  text=str(amount)+" "+seleC   
  neXtxt("t5",text) 
  neXtxt("t8",wallAdrLTC[:7]+"..."+wallAdrLTC[-7:])
  #am =0.0112233
  displayQR(slowZeroW,"litecoin:"+wallAdrLTC+"?amount="+str(amount))
  
 cntWait=0
 cntWait2=0
 time.sleep(2) 
  
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
 
 time.sleep(3) 
 neXcmd("page blockch")
 pip1()
 neXcmd("page blockch")
 time.sleep(3) 
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
   
  time.sleep(2)
  #nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  dtServer = datetime.datetime.strptime(getServerTime(), '%Y-%m-%d %H:%M:%S')
  #dtServerS = dtServer[-8:]
  dtDevice = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
  
  #timDelta= int(nowTime)-int(txsTime)   
  
  neXtxt("tb2",txAmount)
  neXtxt("tb3","serverTime: "+str(dtServer)[-8:]) 
  neXtxt("tb4","deviceTime:  "+str(dtDevice)[-8:])
  time.sleep(2)
  neXtxt("tb5","Blockchain info testing | "+ver) 
  neXtxt("tb6","server: "+str(dtServer)) 
  neXtxt("tb7","device:  "+str(dtDevice)) 
  neXtxt("tb8"," ") 
  time.sleep(2)
  ##neXtxt("tb9","transactionT "+transTime)
  
  
  #------------------------ tx validation:
  
 
  for validLoop in range(8):
     print("--- valid Loop" + str(validLoop))      
     
     deltaMinVal=oneValidation()
     okTrans=False
     if(deltaMinVal<1.1):
       pip1()  
       okTrans=True 
       okTxt= ".....OK..... "+ " | "+str(deltaMinVal)+ " min."
       neXtxt("tb9",okTxt)
       break
     else:       
       neXtxt("tb9",str(validLoop))
       time.sleep(2) 
       okTxt= "NO TRANSACTION "+ " | "+str(deltaMinVal)+ " min."
       neXtxt("tb9",okTxt)
     time.sleep(10+validLoop*2)
     
     if(isJmp1()): break    
  
  pip1()
  for okLoop in range(6): 
     neXtxt("tb9",okTxt)
     time.sleep(1)  
     neXtxt("tb9"," ") 	 
     time.sleep(0.5)
     
  neXtxt("tb9",okTxt)

  #nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  #addLog("T-"+nowTim+" | "+str(deltaMin)+ " min. | val:"+str(transValue)+" s")	 
  #addLog("> K:"+str(lastNum)+", $"+str(valUSD)+", a:"+str(amountS)+" s")	 	    
  #time.sleep(3) 
  #while (not isJmp1()): #waiting to press butt
  #    time.sleep(0.5)
  #    print("."),

  
  if okTrans: 
     addLog(">>"+str(valUSD)+"$ /" +  seleC)
     neXcmd("page thanks")
     pip1()
     neXcmd("page thanks")
     time.sleep(3)          
     
     """
     #------ action
     addLog(">> OK > "+str(valUSD*25)+" Kc"  )
     netLog("OkKc","BTC",valUSD*25)
     
     
     GPIO.output(RELE1, False)
     time.sleep(10)
     GPIO.output(RELE1, True)
     
      
     time.sleep(3)
     neXtxt("tt1","$ "+str(valUSD))     
     time.sleep(3)
     """
       
     while (not isJmp1()):
         time.sleep(0.5)
         #nowTim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         #neXtxt("tb7","date Time:  "+str(nowTim)) 
         neXtxt("tb8","for next action > press BUTTON ") 
         neXtxt("tt2","next") 
		 
         time.sleep(0.5)
         neXtxt("tt2","prew")
         neXtxt("tb8"," ") 
      
  
 #=====================================================================================================

if __name__ == "__main__":
    #try:
       #alarmLoop()
       #thrnx.stop_here
            #try:
            #except:
            #	print "FD config err."
            
     print("------------------------one Start")    
     
     neXcmd("page intro")
     #pip1()
     neXcmd("page intro")
     neXtxt("t0","start > init")
     time.sleep(2)
     pip2()
     neXtxt("t0","please wait")
     time.sleep(2)
     i=0
     numi = 10
     while i<numi:
        print(i)
        neXtxt("t0","BOOT "+str(numi-i))
        i +=1
        time.sleep(2)
     neXtxt("t0"," ")  
     
     time.sleep(10)
     while True:                  
          oneLoop()
          
    #except:
    #    Err = True
    #except (KeyboardInterrupt, SystemExit), e:
    #	print "oops, error", e
    #	print "trying to gracefully shutdown child thread"
    #	print "stopped?", thrnx.stopped()
    #	thrnx.stop()
    #	print "stopped?", thrnx.stopped()
    #	thrnx.join()

    #print "exiting..."
    #-------------------------end --------------
 