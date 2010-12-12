# UDP server example
import socket
import serial

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("", 5000))

print "UDPServer Waiting for client on port 5000"

ser = serial.Serial('/dev/cu.usbserial-00002006', 19200, timeout=1)

home = "\x01"
clear = "\x0c"

while 1:
	data, address = server_socket.recvfrom(256)
	ser.write(clear);
	ser.write("( " + address[0] + " " + str(address[1]) + " ) said : " + data)

ser.close()
