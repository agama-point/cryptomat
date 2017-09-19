# ------------------------------
# 2017/09 - RPi3 (wifi)
# /dev/ttyAMA0 previously used to access the UART now connects to Bluetooth.
# The miniUART is now available on /dev/ttyS0.
#
#
print("Nextion display write test")
import sys, os, subprocess, time, datetime
import struct

from myWallets import  getWBTC, getWLTC
wallAdrBTC=getWBTC()
wallAdrLTC=getWLTC()

#mport urllib2 #course
#import json
#from socket import gethostname, gethostbyname #getIp
from time import sleep

from socket import gethostname, gethostbyname #getIp
from time import sleep
from threading import Thread 

#---nextion
nxRead="00"
nx1="03"
nx2="04"
nx3="05"
nx4="06"
nx5="07"
nx6="08"
nx7="13"  
nexThread = True

b22 = bytes('"'.encode('ascii'))
#bFF = bytes(str(chr(0xff)).encode('utf-8')) #https://docs.python.org/3/howto/unicode.html
#bFF = (b'\xff', 'iso-8859-1') #https://wiki.python.org/moin/Python3UnicodeDecodeError

#https://stackoverflow.com/questions/35454378/python3-sending-serial-data-to-nextion-display
bFF=struct.pack('B', 0xff)

# ======uart tft serial monitor / nextion===== 9600 / 115200
import serial
s = serial.Serial(port='/dev/ttyS0',baudrate=9600,                                                   
            timeout=3.0,
            xonxoff=False, rtscts=False, 
            writeTimeout=3.0,
            dsrdtr=False, interCharTimeout=None)
# timeout=1.0, bylo 3 ---9600
# co="bauds=115200"
# neXcmd(co)             
# ===============================================

#---nextion 2015/12-
  #simple label (similar arduino test)
def neXcmd(cmd):   
    s.write(bytes(cmd.encode('ascii'))) 
    s.write(bFF)
    s.write(bFF)
    s.write(bFF)
    time.sleep(0.001)

def neXtxt(lab,label):
    #s.write("t0.txt=")
    ###s.write(kam)
    s.write(bytes(lab.encode('ascii')))
    #s.write(".txt=")
    #s.write(bytes(".txt=".encode('ascii')))
    s.write(b".txt=")    
    s.write(b22)
    #s.write("testLAB2")
    s.write(bytes(label.encode('ascii')))
    s.write(b22)
    s.write(bFF)
    s.write(bFF)
    s.write(bFF)
    #s.write("\n")
    #displLab("testLAB raspi 2 " + ver)
    #def n(co):
    #hh.dispWrite(chr(co))
    time.sleep(0.05) 
    
#---------------------------------------------------------------
def displayQR(nextionBool,qrGet):
  global s
  os.system('qrencode -o qrcode.png '+qrGet)
  os.system('qrencode -t ASCII -o qrcode.txt '+qrGet)

  neXcmd("baud=115200")
  time.sleep(1)
  s = serial.Serial(port='/dev/ttyS0',baudrate=115200,
            timeout=3.0, xonxoff=False, rtscts=False,
            writeTimeout=3.0, dsrdtr=False, interCharTimeout=None)

  co="fill 133,25,218,160,WHITE"
  neXcmd(co)
  neXcmd(co)

  time.sleep(1)  #nestihalo..

  f = open('qrcode.txt')
  lines = f.readlines()
  #print "number of lines QR: "+ str(len(lines))
  f.close()
  for i in range(3,len(lines)):
    for j in range(3,73):
        point = lines[i][j:j+1]
        if point=="#":
          #print "*",
          if nextionBool:
             co="fill "+str(135+j*2)+","+str(25+i*4)+",3,4,BLACK"
             neXcmd(co)
          #else:
          #   sdPXYC(330-int(j*2.8),int(i*5)-10,2)
        

  neXcmd("baud=9600")
  time.sleep(1)
  #s = serial.Serial(port='/dev/ttyAMA0',baudrate=9600,
  s = serial.Serial(port='/dev/ttyS0',baudrate=9600,    
            timeout=3.0, xonxoff=False, rtscts=False,
            writeTimeout=3.0, dsrdtr=False, interCharTimeout=None)    
    

def nexth(): ##thread
 global nxRead, nexThread
 s.flushInput()
 cntx=0
 nacti= 7
 while nexThread:     
   try:
    hodnota = s.read(nacti) #7
    print(hodnota)
    iok=2 
    for ii in range (nacti):
     if ((hodnota[ii]).encode("hex")=="65"):
      iok = ii # index      
      nexWrite=((hodnota[iok+2]).encode("hex"))
      nxRead = nexWrite   

           
   except:
    # print "Err.data"
    nic = True   
   
   time.sleep(0.7)
   cntx=cntx+1

def nexRead():
   #global frn #file read nextion
   time.sleep(0.7)
   frn = open(intranetNex,"r")
   nexread = frn.read()
   frn.close()
    
   if (nxRead!="00"):
     return nxRead  
     #fwn = open(intranetNex,"w")  
     #fws.write("00")
     #fws.close()
   else:
     return "99"
   #frn.close()

# thread for reading
#thrnx = Thread(target=nexth)
#thrnx.start()

#-----------------------------------------

neXcmd("page intro")

i=0
while i<3:
  print(i)	
  neXtxt("t0",str(3-i))
  i +=1
  time.sleep(1)
  
neXcmd("page qr")
am =0.0112233
displayQR(True,"litecoin:"+wallAdrLTC+"?amount="+str(am))
 

#-------------------------end --------------
