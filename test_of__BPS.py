from BeaglePositioningSystem import GPS
from time import sleep
BPS = GPS()

for i in range(5):
	BPS.read()
	print '\n'
	print 'You are Tracking: ',BPS.sats,' satellites'
	print 'My Latitude: ',BPS.latDeg, 'degrees, ', BPS.latMin,' minutes, ', BPS.latHem,'hemiphere.'
	print 'My Longitude: ',BPS.lonDeg, 'degrees, ', BPS.lonMin,' minutes, ', BPS.lonHem,'hemiphere.'
	print 'My Speed(in knots): ', BPS.knots
	print 'My Altitude: ',BPS.altitude
	sleep(1)
