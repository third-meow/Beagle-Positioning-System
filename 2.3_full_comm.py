import serial
import Adafruit_BBIO.UART as UART
from time import sleep
UART.setup("UART1")
ser=serial.Serial('/dev/ttyO1',9600)

class GPS:
        def __init__(self):

		#Update means reporting to beaglebone
		UPDATE_10_sec=  "$PMTK220,10000*2F\r\n" 				#Update Every 10 Seconds
                UPDATE_5_sec=  "$PMTK220,5000*1B\r\n"   				#Update Every 5 Seconds
                UPDATE_1_sec=  "$PMTK220,1000*1F\r\n"   				#Update Every One Second
                UPDATE_200_msec=  "$PMTK220,200*2C\r\n" 				#Update Every 200 Milliseconds

		#Measure means contacting satellites and reciveing info
		MEAS_10_sec = "$PMTK300,10000,0,0,0,0*2C\r\n" 				#Measure every 10 seconds
                MEAS_5_sec = "$PMTK300,5000,0,0,0,0*18\r\n"   				#Measure every 5 seconds
                MEAS_1_sec = "$PMTK300,1000,0,0,0,0*1C\r\n"   				#Measure once a second
                MEAS_200_msec= "$PMTK300,200,0,0,0,0*2F\r\n"  				#Meaure 5 times a second

		#Baud rate is setting "highest speed" of serial communication
                BAUD_57600 = "$PMTK251,57600*2C\r\n"          				#Set Baud Rate at 57600
                BAUD_9600 ="$PMTK251,9600*17\r\n"            				#Set 9600 Baud Rate

                GPRMC_ONLY= "$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n" 	#Send only the GPRMC Sentence
                GPRMC_GPGGA="$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n"	#Send GPRMC AND GPGGA Sentences
                SEND_ALL ="$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n" 	#Send All Sentences
                SEND_NOTHING="$PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n" 	#Send Nothing


		ser.write(BAUD_57600)
                sleep(1)
                ser.baudrate=57600
                ser.write(UPDATE_200_msec)
                sleep(1)
                ser.write(MEAS_200_msec)
                sleep(1)
                ser.write(GPRMC_GPGGA)
                sleep(1)
                ser.flushInput()
                ser.flushOutput()
                print "GPS is Initialized"
	def read(self):
	        ser.flushInput()		#clear buffers
	        ser.flushInput()
	       	while ser.inWaiting()==0:	#wait for data
	       	        pass
		self.NMEA1 = ser.readline()	#read first string of data
		while ser.inWaiting()==0:	#wait for more data
			pass
		self.NMEA2 = ser.readline()	#read second string of data

		self.NEMA1_list = self.NEMA1.split(',')		#split NEMAs into lists
		self.NEMA2_list = self.NEMA2.split(',')

		if self.NEMA1_list[0]=='$GPRMC':		#sort NEMA lists into their sentance names
			self.GPRMC = self.NEMA1_list
			self.GPGGA = self.NEMA2_list
		elif self.NEMA1_list[0]=='$GPGGA':
			self.GPRMC = self.NEMA1_list
			self.GPGGA = self.NEMA2_list
		else:
			print '[ERROR][SENTANCE ERROR]'

		self.latDeg = self.GPRMC[3][:-7]
		self.latMin = self.GPRMC[3][-7:]
		self.latHem = self.GPRMC[4]

		self.lonDeg = self.GPRMC[5][:-7]
		self.lonMin = self.GPRMC[5][-7:]
		self.lonHem = self.GPRMC[6]

		self.knots = self.GPRMC[7]
		self.altitude = self.GPGGA[9]

		self.fix = self.GPGGA[6]
		self.sats = self.GPGGA[7]

myGPS=GPS()
try:
	while(1):
		myGPS.read()
                print 'You are Tracking: ',myGPS.sats,' satellites'
                print 'My Latitude: ',myGPS.latDeg, 'Degrees ', myGPS.latMin,' minutes ', myGPS.latHem
                print 'My Longitude: ',myGPS.lonDeg, 'Degrees ', myGPS.lonMin,' minutes ', myGPS.lonHem
                print 'My Speed(in knots): ', myGPS.knots
                print 'My Altitude: '
myGPS.altitude
except KeyboardInterrupt:
	print('\n\n GoodBye \n')
