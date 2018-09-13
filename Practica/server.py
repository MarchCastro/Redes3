#!usr/bin/python

#block_server.py

import socket

s = socket.socket()

host = socket.gethostname()
port = 12345

s.bind((host,port))
s.listen(5)

while True:
	conn, addr = s.accept()		# accept the connection
	#print "Address:",addr

	data = conn.recv(1024)	
	while data:
		print "DATA",data 
		data = conn.recv(1024)
        splitData = data.split(',')
        print splitData
	print "All Data Received"	# Will execute when all data is received
    
    
    #print splitData
	conn.close()
	break