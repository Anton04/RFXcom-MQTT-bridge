#!/usr/bin/python

from RFXtrx.pyserial import PySerialTransport
from RFXtrx import LightingDevice
import mosquitto,sys
import json
import thread
import time
from RFXtrx.lowlevel import Lighting2 

PORT = '/dev/ttyUSB0'
LISTEN = True
PREFIX = "rfxcom"
MQTT_HOST = "localhost"

def on_connect(mosq, rc,a):
    mosq.subscribe(PREFIX+"/#", 0)

def on_message(a,mosq, msg):
    global transport
    try:
   
    	print("RECIEVED MQTT MESSAGE: "+msg.topic + " " + str(msg.payload))
    	topics = msg.topic.split("/")
    	name = topics[-2]
    	if topics[-1] == "set":
	    value = msg.payload.upper()
	    if value == "ON":
		value = 100
	    elif value == "OFF":
                value = 0
    	    value = int(value)
    	    #print "Set command"

    	    #Implemented support for Lightening2 only
	    if topics[-4] == "17":
		print "Seting Lighting2 level" 
		print topics
		print value
		pkt = Lighting2()
		#pkt.parse_id(topics[-3],topics[-2])
		code = topics[-2].split(":")
		pkt.id_combined = int(code[0],16)
		pkt.unitcode = int(code[1])
		pkt.subtype = int(topics[-3])
		pkt.packettype = int(topics[-4])
		device = LightingDevice(pkt)
		if value == 0:
		    device.send_off(transport)
		elif value == 100:
		    device.send_on(transport)
		else:
		    device.send_dim(transport,value)
    except:
        print "Error when parsing incomming message."
    
    return 
    
def ControlLoop():
    # schedule the client loop to handle messages, etc.
    print "Starting MQTT listener"
    while True:
        client.loop()
        time.sleep(0.1)

transport = PySerialTransport(PORT, debug=True)
#transport.reset()
client = mosquitto.Mosquitto("RFXcom-to-MQTT-client")
client.username_pw_set("anton","1234")

#Connect and notify others of our presence. 
client.connect(MQTT_HOST)
client.publish("system/RFXcom-to-MQTT", "Online",1)
client.on_connect = on_connect
client.on_message = on_message

#Start tread...
thread.start_new_thread(ControlLoop,())

while True:
    event = transport.receive_blocking()

    if event == None:
	continue
    
    for value in event.values:
   
        topic = PREFIX +"/"+ str(event.device.packettype) + "/" + str(event.device.subtype) + "/" + event.device.id_string+"/"+value

	print topic + " " + str(event.values[value])

	#print "DEBUG"
	#print event.device.id_combined
	#print event.device.unitcode    

        client.publish(topic , event.values[value], 1)
    
    	print event 
    
    
client.disconnect() 


