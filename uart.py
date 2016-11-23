import serial

byte = b'G'	# character 'G'
buildString, celciusH, celciusL = [], [], []

ser = serial.Serial('/dev/ttyACM0',baudrate=9600,bytesize=8, parity='N', stopbits=1, timeout=None)
print(ser.name)         # check which port was really used
#byte.encode('ascii')

while True:
	temperature = 0
	for p in range(1, len(celciusH),1):
		celciusH[p] = 0
	for t in range(1, len(celciusL),1):
		celciusL[t] = 0
	print("sending 'G' char as: ", byte)
	ser.write(b'G')     # write a string

	#byte.encode('ascii')
	#print("sending 'G' char as: ", byte)
	#ser.write(b"byte")     # write a string
	print("reading response, how many bytes?")
	userinput = input()  #accepts user txt file input
	bytes = int(userinput)
	print(bytes)

	# for val in range(1,int(userinput),1):
		# print("try")
		# buildString.append(ser.read(int(userinput)))
		# print(val)		
		# temperature = ''.join(l)

	temperature = ser.read(bytes)
	if temperature.decode("utf-8") == 'K':
		celciusH.append(ser.read(2))
		#celciusH = int(celciusH.strip(''))
		period = ser.read(1)
		period = period.decode("utf-8")
		celciusL.append(ser.read(2))
		print("celsius = : ",celciusH, period, celciusL)

	print("returned val: ",temperature.decode("utf-8"))

print("quit")
ser.close()             # close port
