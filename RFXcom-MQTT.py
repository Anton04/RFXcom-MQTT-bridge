from RFXtrx.pyserial import PySerialTransport
import mosquitto,sys

transport = PySerialTransport('/dev/ttyUSB0', debug=True)
transport.reset()

while True:
    event = transport.receive_blocking()
    
    print event 
