#!/usr/bin/env python
import socket
import sys
import serial
import time
import os
import requests
import json,time,string
apiheaders={'U-ApiKey':'48d940310bac0516d988c73846f20a8a','content-type':'application/json'}
humid_apiurl="http://api.yeelink.net/v1.0/device/350903/sensor/394064/datapoints" 

def scanMessage():
    rcv=port.readline()
    if(rcv[0:4]=="+CMT"):
        rcv=port.readline()
        return rcv
    else:
        return ""
    
def sendMessage(num,text):
    port.write('AT+CMGS="'+num.encode()+'"\r')
    time.sleep(1)
    port.write(text.encode()+"\x1a")
    time.sleep(1)

farmer="+18582297233"
port=serial.Serial("/dev/ttyUSB0",baudrate=115200,timeout=1)
port.write('ATH')
rcv=port.readline()
print(rcv)
time.sleep(1)
port.write('AT+CMGF="1"\r')
rcv=port.readline()
print(rcv)
time.sleep(1)
port.write('AT+CNMI=1,2,0,0,0\r')
rcv=port.readline()
print(rcv)
time.sleep(1)


msgSent=False
engine = True
TCP_IP = '192.168.137.250'
TCP_PORT = 4444
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("starting Station")

s.bind((TCP_IP, TCP_PORT))
s.listen(1)

connection, client_address = s.accept()
    


try:
    print >>sys.stderr, 'connection from', client_address

    while True:
        SMS=scanMessage()
        if(SMS.rstrip()=='On'):
            #turn on/off
            print("ONNNNN by phone")
            connection.sendall("$")
            engine =True
            msgSent = False
            #if on
        if(SMS.rstrip()=='Off'):
            print("OFFFFFF by phone")
            #if off
            connection.sendall("%")
            msgSent = False
        data = connection.recv(BUFFER_SIZE)
        
        if data:
            print ('moisture:'+data)
            if (data.isdigit()):
                humid_payload={'value':int(data)}
                r=requests.post(humid_apiurl,headers=apiheaders,data=json.dumps(humid_payload))
                numData = int(data);
                
                if (numData<20 and engine==False):
                    if(msgSent==False):
                        sendMessage(farmer,"Hey I'm thirsty! Where's my booze at?")
                        msgSent=True
                    
                    #connection.sendall("111")
                    #print('turning LED on')
                    
                if (numData>80 and engine==True):
                    if(msgSent==False):
                        sendMessage(farmer,"So drunk! Cut the supply")
                        msgSent=True
                    #connection.sendall("222")
                    #print('turning LED off')
            
        else:
            print >>sys.stderr, 'no more data from', client_address
            break
            
finally:
    # Clean up the connection
    connection.close()
