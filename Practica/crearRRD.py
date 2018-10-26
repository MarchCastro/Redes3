#!/usr/bin/env python

import rrdtool
'''
HW create 
'''

def crear(nombre):
	ret = rrdtool.create(nombre,
		                 "--start",'1537228800',
		                 "--step",'10',
		                 "DS:inoctets:COUNTER:600:U:U",
		                 "DS:outoctets:COUNTER:600:U:U",
		                 "DS:establishedtcpconn:GAUGE:600:U:U",
		                 "DS:intcpsegs:COUNTER:600:U:U",
		                 "DS:outtcpsegs:COUNTER:600:U:U",
		                 "DS:inicmpmsgs:COUNTER:600:U:U",
		                 "DS:outicmpmsgs:COUNTER:600:U:U",
		                 "DS:insnmpresponses:COUNTER:600:U:U",
		                 "DS:outsnmpresponses:COUNTER:600:U:U",		                                                   
		                 "RRA:AVERAGE:0.5:6:700",
		                 "RRA:AVERAGE:0.5:1:600")

	if ret:
		print rrdtool.error()
		
def crearLB(nombre,num_cores):
	#Agrega parametros a rrd
	rrdStr = [nombre, "--start",'N', "--step",'10']
	#Agrega variable porcentaje de ram usado
	rrdStr += ["DS:ramused:GAUGE:600:U:U"]
	#Agrega variable porcentaje de HDD usado
	rrdStr += ["DS:hddused:GAUGE:600:U:U"]	
	#Agrega variable porcentaje de uso de cada core
	for i in range(1,num_cores+1):
		rrdStr += ["DS:CORE"+str(i)+":GAUGE:600:U:U"]
	rrdStr += ["RRA:AVERAGE:0.5:6:700"]
	rrdStr += ["RRA:AVERAGE:0.5:1:600"]
	#Crea la rrd
	ret = rrdtool.create(rrdStr)
	if ret:
		print rrdtool.error()

def crearHW(nombre):
	print 'NOMBREEE '+nombre

	ret = rrdtool.create(nombre,
						"--start",'N',
						"--step",'60',
						"DS:inoctets:COUNTER:600:U:U",
						"DS:outoctets:COUNTER:600:U:U",
						"RRA:AVERAGE:0.5:1:1209",
						"RRA:HWPREDICT:600:0.9:0.0035:172:3",
						"RRA:SEASONAL:172:0.9:2",
						"RRA:DEVSEASONAL:172:0.9:2",
						"RRA:DEVPREDICT:600:4",
						"RRA:FAILURES:172:7:9:4") 
	if ret:
		print rrdtool.error()

"""def crearHW(nombre):
	print 'NOMBREEE '+nombre
	ret = rrdtool.create(nombre,
						"--start",'N',
						"--step",'60',
						"DS:inoctets:COUNTER:600:U:U",
						"DS:outoctets:COUNTER:600:U:U",
						"DS:establishedtcpconn:GAUGE:600:U:U",
						"DS:intcpsegs:COUNTER:600:U:U",
						"DS:outtcpsegs:COUNTER:600:U:U",
						"DS:inicmpmsgs:COUNTER:600:U:U",
						"DS:outicmpmsgs:COUNTER:600:U:U",
						"DS:insnmpresponses:COUNTER:600:U:U",
						"DS:outsnmpresponses:COUNTER:600:U:U",	
						"RRA:AVERAGE:0.5:1:20",
						"RRA:HWPREDICT:50:0.1:0.0035:10:3",                      
						"RRA:SEASONAL:10:0.1:2", 
						"RRA:DEVSEASONAL:10:0.1:2",
						"RRA:DEVPREDICT:50:4",
						"RRA:FAILURES:50:7:9:4") 
	if ret:
		print rrdtool.error()"""

if __name__ == '__main__':
	crear("127.0.0.1-net.rrd")
