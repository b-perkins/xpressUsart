import serial

byte = b'G'	# character 'G'
ser = serial.Serial('/dev/ttyACM0',baudrate=9600,bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
print(ser.name)         # check which port was really used

print("sending 'G' char as: ", byte)
ser.write(b"byte")     # write a string

byte.encode('ascii')
print("sending 'G' char as: ", byte)
ser.write(b"byte")     # write a string
print("reading response")
s = ser.read(100)
print("returned val: ",s)
ser.close()             # close port
