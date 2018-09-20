#!/usr/bin/env python

import rrdtool
'''
Script que crea la base de datos rrdtool para almacenar las 5 variables eleginas por el equipo:
	
1537228800 = 18 DE SEPTIEMBRE DEL 2018 A LAS 00

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

if __name__ == '__main__':
	crear("127.0.0.1-net.rrd")
