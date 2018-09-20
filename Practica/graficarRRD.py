import sys
import rrdtool
import time
tiempo_actual = int(time.time())
tiempo_final = tiempo_actual - 86400
tiempo_inicial = tiempo_final -25920000
tiempo_graficacion = str(1537404600) # tiempo del 19 de septiembre a las 18

'''
Este script genera una grafica en PNG a partir de la base de datos net3.rrd creada
por el script rrd1.py y actualizada por rrd2.py


 "--vertical-label=Bytes/s",  #etiqueta del eje y
 "DEF:inoctets=net3.rrd:inoctets:AVERAGE", #nombre inoctets
 "DEF:outoctets=net3.rrd:outoctets:AVERAGE", #nombre outoctets
 "AREA:inoctets#00FF00:In traffic",
 "LINE1:outoctets#0000FF:Out traffic\r")
'''


def graficar(cadena,rrd,image_name,id_grafica):

	if id_grafica == 1:	
		while 1:
			print cadena
			ret = rrdtool.graph( image_name,
				             "--start",tiempo_graficacion, 
		 #                    "--end","N",
				             "--vertical-label=Bytes/s",
				             "DEF:inoctets="+rrd+":inoctets:AVERAGE",
				             "DEF:outoctets="+rrd+":outoctets:AVERAGE",
				             "AREA:inoctets#00FF00:In traffic",
				             "LINE1:outoctets#0000FF:Out traffic\r")

			time.sleep(5)
	elif id_grafica == 2:
		while 1:
			print cadena
			ret = rrdtool.graph( image_name,
				             "--start",tiempo_graficacion,
		 #                    "--end","N",
				             "--vertical-label=Numero de conexiones",
				             "DEF:establishedtcpconn="+rrd+":establishedtcpconn:AVERAGE",
				             "LINE1:establishedtcpconn#0000FF:Conexiones TCP establecidas\r")

			time.sleep(5)
	elif id_grafica == 3:
		while 1:
			print cadena
			ret = rrdtool.graph( image_name,
				             "--start",tiempo_graficacion,
		 #                    "--end","N",
				             "--vertical-label=TCP Segs/s",
				             "DEF:intcpsegs="+rrd+":intcpsegs:AVERAGE",
				             "DEF:outtcpsegs="+rrd+":outtcpsegs:AVERAGE",
				             "AREA:intcpsegs#00FF00:In TCP traffic",
				             "LINE1:outtcpsegs#0000FF:Out TCP traffic\r")

			time.sleep(5)
	elif id_grafica == 4:
		while 1:
			print cadena
			ret = rrdtool.graph( image_name,
				             "--start",tiempo_graficacion,
		 #                    "--end","N",
				             "--vertical-label=ICMP msgs/s",
				             "DEF:inicmpmsgs="+rrd+":inicmpmsgs:AVERAGE",
				             "DEF:outicmpmsgs="+rrd+":outicmpmsgs:AVERAGE",
				             "AREA:inicmpmsgs#00FF00:In ICMP msgs",
				             "LINE1:outicmpmsgs#0000FF:Out ICMP msgs\r")

			time.sleep(5)
	elif id_grafica == 5:
		while 1:
			print cadena
			ret = rrdtool.graph( image_name,
				             "--start",tiempo_graficacion,
		 #                    "--end","N",
				             "--vertical-label=SNMP PDUs/s",
				             "DEF:insnmpresponses="+rrd+":insnmpresponses:AVERAGE",
				             "DEF:outsnmpresponses="+rrd+":outsnmpresponses:AVERAGE",
				             "AREA:insnmpresponses#00FF00:Solicitudes",
				             "LINE1:outsnmpresponses#0000FF:Respuestas\r")

			time.sleep(5)
	else:
		print "Error en la graficacion"				
		
if __name__ == '__main__':
	graficar("Graficando...")
