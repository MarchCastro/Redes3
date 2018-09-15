#!usr/bin/python

# non_blocking_client.py

import socket

sock = socket.socket()

print "Bienvenido :D"

community = raw_input("Introduce tu comunidad SNMP: ")
version = raw_input("Introduce tu version SNMP: ")
port = int(input("Introduce tu puerto: "))
print community, version, port
#host = socket.gethostname()
sock.connect(('10.100.78.176', port))
sock.setblocking(0)      # Now setting to non-blocking mode

cadena = str(port)+' '+community+' '+version
print 'Cadena',cadena

data = cadena  # Huge amount of data to be sent
assert sock.send(data)              # Send data till true
#https://www.studytonight.com/network-programming-in-python/blocking-and-nonblocking-socket-io


#SERVER
def main():
	sock = socket.socket()

	#host = socket.gethostname()
	host = '0.0.0.0'
	port = 12345

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((host, port))
	#s.bind((host,port))
	sock.listen(5)


	while True:
		conn, addr = sock.accept()		# accept the connection
		#print "Address:",addr
		file = open("hosts.txt","a+")
		data = conn.recv(1024)	
		print data 
		file.write(data)
		file.write('\n')
		file.close()
		#splitData = data.split('$')
		splitData = data.split(' ')
		print splitData
		


		print "All Data Received"	# Will execute when all data is received
		#print splitData
		#conn.close()
		#break