#!usr/bin/python

# non_blocking_client.py

import socket

sock = socket.socket()

print "Bienvenido :D"

community = raw_input("Introduce tu comunidad SNMP: ")
version = raw_input("Introduce tu version SNMP: ")
port = int(input("Introduce tu puerto: "))
print community, version, port
host = socket.gethostname()
sock.connect((host, port))
sock.setblocking(0)			# Now setting to non-blocking mode

cadena = socket.gethostbyname(host)+','+str(port)+','+community+','+version
print 'Cadena',cadena

data = cadena	# Huge amount of data to be sent
assert sock.send(data)			        # Send data till true
#https://www.studytonight.com/network-programming-in-python/blocking-and-nonblocking-socket-io