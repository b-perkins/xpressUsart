import serial
import subprocess

celsiusH, celsiusL = 0, 0
celsius = ""
fahrenheit = 0.0

# ser = serial.Serial('COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None)	#	If on win
ser = serial.Serial('/dev/ttyACM0',baudrate=9600,bytesize=8, parity='N', stopbits=1, timeout=None)	#	linux
resulttxt = open("/dev/shm/mjpeg/user_annotate.txt", "w")	#the output file

ser.write(b'G')  # write charg G as a byte

startBit = ser.read(1)  # Read 1 byte
if startBit.decode("utf-8") == 'K':  # K means the next to chars will be temp hi/lo
	celsiusH = ser.read(1)
	celsiusL = ser.read(1)
	celsiusH = ord(celsiusH)	#converts to integer
	celsiusL = ord(celsiusL)

	celsius += str(celsiusH)	#create a decimal string
	celsius += '.'
	celsius += str(celsiusL)

	fahrenheit = (float(celsius)*9) / 5.0 + 32	#convert to fahrenheit (needs float)

	resulttxt.write(str(fahrenheit))
	resulttxt.close()			#note - txt doesnt show up unless file is closed

ser.close()  # close port
