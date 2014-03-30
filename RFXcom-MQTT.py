from RFXtrx.pyserial import PySerialTransport
import mosquitto,sys
import json

transport = PySerialTransport('/dev/ttyUSB0', debug=True)
transport.reset()

MQTT_HOST = "localhost"

client = mosquitto.Mosquitto("plug-client")
client.connect(MQTT_HOST)

client.publish("system/RFXcom-MQTT", 1,1)

while True:
    event = transport.receive_blocking()
    
    value = json.dumps(event.values)

    topic = "rfxcom/" + event.device.type_string + "/" + event.device.id_string

    print topic
    
    client.publish(topic , value, 1)
    
    print event 
    
    
client.disconnect() 


