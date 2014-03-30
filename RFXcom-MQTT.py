from RFXtrx.pyserial import PySerialTransport
import mosquitto,sys
import json

PORT = '/dev/ttyUSB0'
LISTEN = True
PREFIX = "rfxcom"
MQTT_HOST = "localhost"


transport = PySerialTransport(PORT, debug=True)
#transport.reset()
client = mosquitto.Mosquitto("RFXcom-to-MQTT-client")


#Connect and notify others of our presence. 
client.connect(MQTT_HOST)
client.publish("system/RFXcom-to-MQTT", "Online",1)


while True:
    event = transport.receive_blocking()
    
    value = json.dumps(event.values)

    topic = PREFIX + event.device.packettype + "/" + event.device.type_string + "/" + event.device.id_string

    print topic
    
    client.publish(topic , value, 1)
    
    print event 
    
    
client.disconnect() 


