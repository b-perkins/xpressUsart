import serial
import subprocess

celciusH, celciusL = 0, 0

ser = serial.Serial('COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=None)	#	If on win
# ser = serial.Serial('/dev/ttyACM0',baudrate=9600,bytesize=8, parity='N', stopbits=1, timeout=None)	#	linux
print(ser.name)  # check which port was really used
resulttxt = open("temp.txt", "w")	#the output file

while True:
	celciusH, celciusL = 0, 0
	print("Beginning - ping device by sending 'G' char. Waiting...")
	goBIT = input()
	if goBIT == 'G':
		ser.write(b'G')  # write charg G as a byte

	startBit = ser.read(1)  # Read 1 byte
	if startBit.decode("utf-8") == 'K':  # K means the next to chars will be temp hi/lo
		celciusH = ser.read(1)
		celciusL = ser.read(1)
		celciusH = ord(celciusH)
		celciusL = ord(celciusL)

		print("temp is: ", celciusH, ".", celciusL)
		resulttxt.write(str(celciusH))
		resulttxt.write(".")
		resulttxt.write(str(celciusL))
		resulttxt.close()

		lookingForL = ser.read(1)
		if lookingForL.decode("utf-8") == 'L':
			print("DONE")
		else:
			print("something's not right")
	else:
		print("expected begginging char K but didnt get it")

print("quit")
ser.close()  # close port
