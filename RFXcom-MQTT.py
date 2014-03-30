from RFXtrx.pyserial import PySerialTransport
import mosquitto,sys

transport = PySerialTransport('/dev/ttyUSB0', debug=True)
transport.reset()

MQTT_HOST = "localhost"

client = mosquitto.Mosquitto("plug-client")
client.connect(MQTT_HOST)



while True:
    event = transport.receive_blocking
    
    value = 1
    
    client.publish("rfxcom/" + event.device.type_string + "/" + event.device.id_string , value, 1)
    
    print event 
    
    
client.disconnect() 


