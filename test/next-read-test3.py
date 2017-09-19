# ------------------------------
# 2017/09 - RPi3 (wifi)
# /dev/ttyAMA0 previously used to access the UART now connects to Bluetooth.
# The miniUART is now available on /dev/ttyS0.
#
#
print("Nextion display write test")
import sys, os, subprocess, time, datetime
import struct

#mport urllib2 #course
#import json
#from socket import gethostname, gethostbyname #getIp
from time import sleep

from socket import gethostname, gethostbyname #getIp
from time import sleep
from threading import Thread 

#---nextion
nxRead="00"
nx1=b'\x03' #struct.pack('B', 0x03)
nx2=b'\x04' #struct.pack('B', 0x04)
nx3=b'\x05'
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
b65=struct.pack('B', 0x65)

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
    #hodnotaStr = hodnota.decode('utf-8')
    #print(hodnotaStr +"***")
    """
    iok=2 
    for ii in range (nacti):
     #if ((hodnota[ii]).encode("hex")=="65"):
     if ((hodnota[ii])==b65):    
      iok = ii # index      
      nexWrite=((hodnota[iok+2]).encode("hex"))
      nxRead = nexWrite   
    """ 
           
   except:
    # print "Err.data"
    nic = True   
   
   time.sleep(0.3)  #0.7)
   cntx=cntx+1


# thread for reading
thrnx = Thread(target=nexth)
thrnx.start()

#-----------------------------------------

neXcmd("page intro")

i=0
while i<3:
  print(i)	
  neXtxt("t0",str(3-i))
  i +=1
  time.sleep(0.3)
  
neXcmd("page select")








#--------------------------------------------------------------------------------

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
         print("nx1")
         cekej = False
     if (ctu==nx2):
         print("nx2")
         cekej = False
     if (ctu==nx3):
         print("nx3")
         cekej = False    
         
     #else: 
     #   print("---nic----" + ctu)
     #   nic = True
     time.sleep(0.7)
 
time.sleep(2) 
ctu = ""
cekej = True
ccnt=0
while cekej: #cekani na stisk
     ccnt=ccnt+1
     ctu = nxRead
     #neXtxt("d0",str(ccnt) + ">"+str(ctu))
     neXtxt("d0",str(ccnt))    
     ###pip(1800,0.05) #ctu    
     if (ctu==nx1):
         print("nx1")
         cekej = False
     if (ctu==nx2):
         print("nx2")
         cekej = False
     #if (ctu==nx3):
     #    print("nx3")
     #    cekej = False 
     
     time.sleep(0.7)


#-------------------------end --------------
