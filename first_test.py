print 'Place:SETUP'
import serial
import Adafruit_BBIO.UART as UART
UART.setup('UART1')
GPS = serial.Serial('/dev/ttyO1', 9600)
NEMA = 'nothing'
while(1):
	print 'Place:WAITING'
	while GPS.inWaiting()==0:
		pass
	print 'Place:READING'
	NMEA=GPS.readline()
	print 'Place:PRINTING'
	print NEMA

