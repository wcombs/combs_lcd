# UDP client example
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
	data = raw_input("Type something(q or Q to exit): ")
	if (data <> 'q' and data <> 'Q'):
		client_socket.sendto(data, ("localhost",5000))
	else:
		break
client_socket.close()
