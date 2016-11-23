import serial

byte = b"G"	# character 'G'
buildString = []

ser = serial.Serial('/dev/ttyACM0',baudrate=9600,bytesize=8, parity='N', stopbits=1, timeout=None)
print(ser.name)         # check which port was really used
#byte.encode('ascii')

while True:
	print("sending 'G' char as: ", byte)
	ser.write(byte)     # write a string

	#byte.encode('ascii')
	#print("sending 'G' char as: ", byte)
	#ser.write(b"byte")     # write a string
	print("reading response")
	for val in range(0,5,1):
		s = ser.read(1)
		buildString.append(s)
	temperature = ''.join(l)
	print("returned val: ",temperature)

print("quit")
ser.close()             # close port
