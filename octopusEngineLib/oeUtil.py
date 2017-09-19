import time, datetime
#from datetime import datetime
#from urllib import urlopen
import urllib
import requests 
import json  


#---server time--- (start > RPi was off-line)
def getServerTime():
   serverTime = urllib.request.urlopen("http://www.octopusengine.eu/api/datetime.php").read()
   return str(serverTime.decode('ascii'))

def addLog(txtLog):
  print("LOG:"+txtLog)
  fw = open("log.txt","a")
  fw.write(txtLog+"\n")
  fw.close()