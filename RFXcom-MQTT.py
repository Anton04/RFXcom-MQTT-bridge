from RFXtrx.pyserial import PySerialTransport
import mosquitto,sys
import json
import thread

PORT = '/dev/ttyUSB0'
LISTEN = True
PREFIX = "rfxcom"
MQTT_HOST = "localhost"

def on_connect(mosq, rc):
    mosq.subscribe(PREFIX+"/#", 0)

def on_message(mosq, msg):
    print("RECIEVED MQTT MESSAGE: "+msg.topic + " " + str(msg.payload))
    topics = msg.topic.split("/")
    name = topics[-2]
    if topics[-1] == "set":
    value = int(msg.payload)
    
    #TODO Create device and set value
    
    return value 
    
def ControlLoop():
    # schedule the client loop to handle messages, etc.
    print "Starting MQTT listener"
    while True:
        client.loop()
        time.sleep(0.1)

transport = PySerialTransport(PORT, debug=True)
#transport.reset()
client = mosquitto.Mosquitto("RFXcom-to-MQTT-client")


#Connect and notify others of our presence. 
client.connect(MQTT_HOST)
client.publish("system/RFXcom-to-MQTT", "Online",1)
client.on_connect = on_connect
client.on_message = on_message

#Start tread...
thread.start_new_thread(ControlLoop,())

while True:
    event = transport.receive_blocking()
    
    value = json.dumps(event.values)

    topic = PREFIX + event.device.packettype + "/" + event.device.type_string + "/" + event.device.id_string

    print topic
    
    client.publish(topic , value, 1)
    
    print event 
    
    
client.disconnect() 


