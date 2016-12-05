import serial
import subprocess

celsiusH, celsiusL = 0, 0
celsius = ""
fahrenheit = 0.0
go = True

# ser = serial.Serial('COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None)	#	If on win
ser = serial.Serial('/dev/ttyACM0',baudrate=9600,bytesize=8, parity='N', stopbits=1, timeout=None)	#	linux
print(ser.name)  # check which port was really used
resulttxt = open("/dev/shm/mjpeg/user_annotate.txt", "w")	#the output file

while go:
	celsiusH, celsiusL = 0, 0
	print("Beginning - ping device by sending 'G' char. Waiting...")
	goBIT = input()
	if goBIT == 'G':
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
		print("tempString in C = ",celsius)
		fahrenheit = (float(celsius)*9) / 5.0 + 32	#convert to fahrenheit (needs float)
		print("temp in F = ", fahrenheit)
		resulttxt.write(str(fahrenheit))
		resulttxt.close()			#note - txt doesnt show up unless file is closed

		lookingForL = ser.read(1)
		if lookingForL.decode("utf-8") == 'L':	#arbitrary stop character
			print("DONE")
			go = False
		else:
			print("something's not right")
	else:
		print("expected begginging char K but didnt get it")

print("quit")
ser.close()  # close port
