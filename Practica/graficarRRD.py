import sys
import rrdtool
import time
tiempo_actual = int(time.time())
tiempo_final = tiempo_actual + 1800
tiempo_inicial = tiempo_actual - 1800
tiempo_graficacion = str( 1538157600) # tiempo del 28 de septiembre a las 18

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
				             "--start",str(tiempo_inicial),
		                     "--end",str(tiempo_final),
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
				             "--start",str(tiempo_inicial),
		                     "--end",str(tiempo_final),
				             "--vertical-label=Numero de conexiones",
				             "DEF:establishedtcpconn="+rrd+":establishedtcpconn:AVERAGE",
				             "LINE1:establishedtcpconn#0000FF:Conexiones TCP establecidas\r")

			time.sleep(5)
	elif id_grafica == 3:
		while 1:
			print cadena
			ret = rrdtool.graph( image_name,
				             "--start",str(tiempo_inicial),
		                     "--end",str(tiempo_final),
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
				             "--start",str(tiempo_inicial),
		                     "--end",str(tiempo_final),
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
				             "--start",str(tiempo_inicial),
		                     "--end",str(tiempo_final),
				             "--vertical-label=SNMP PDUs/s",
				             "DEF:insnmpresponses="+rrd+":insnmpresponses:AVERAGE",
				             "DEF:outsnmpresponses="+rrd+":outsnmpresponses:AVERAGE",
				             "AREA:insnmpresponses#00FF00:Solicitudes",
				             "LINE1:outsnmpresponses#0000FF:Respuestas\r")

			time.sleep(5)
	else:
		print "Error en la graficacion"				

def graficar_HW(cadena,rrd,image_name,id_grafica):
	print cadena
	print rrd
	print image_name
	print id_grafica
	if id_grafica == 1:	
		while 1:
			ret = rrdtool.graph(image_name,
                        "--start", str(rrdtool.last(rrd)-3600),
                        "--end",str(rrdtool.last(rrd)),
                        "--vertical-label=Bytes/s",
                        #Declaro cada valor que quiero mostrar en grafica
						"DEF:obs="+rrd+":inoctets:AVERAGE",
                        "DEF:outoctets="+rrd+":outoctets:AVERAGE",
                        "DEF:pred="+rrd+":inoctets:HWPREDICT",
                        "DEF:dev="+rrd+":inoctets:DEVPREDICT",
                        "DEF:fail="+rrd+":inoctets:FAILURES",

                        "CDEF:scaledobs=obs,8,*", #los valores obsevados, los multiplico *8
						"CDEF:scaledout=outoctets,8,*", #los valores obsevados, los multiplico *8
                        "CDEF:upper=pred,dev,2,*,+",#limite superior                        
                        "CDEF:lower=pred,dev,2,*,-",#limite inferior
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "CDEF:scaledpred=pred,8,*",
                        "LINE1:scaledobs#00FF00:In traffic",
                        "LINE1:scaledout#0000FF:Out traffic",
                        "TICK:fail#FDD017:1.0:  Fallas",
                        "LINE1:scaledpred#FF00FF:Prediccion",
						"LINE1:scaledupper#00e4ef:Upper Bound Average out bits",
                        "LINE1:scaledlower#ff0000:Lower Bound Average out bits")
    		time.sleep(1)
	"""elif id_grafica == 2:	
		while 1:
			ret = rrdtool.graph(image_name,
                        "--start", str(rrdtool.last(rrd)-1800),#'1479434100',
                        "--end",str(rrdtool.last(rrd)),
                        "--vertical-label=Numero de conexiones",
                        #Declaro cada valor que quiero mostrar en grafica
						"DEF:establishedtcpconn="+rrd+":establishedtcpconn:AVERAGE",
                        "DEF:pred="+rrd+":establishedtcpconn:HWPREDICT",
                        "DEF:dev="+rrd+":establishedtcpconn:DEVPREDICT",
                        "DEF:fail="+rrd+":establishedtcpconn:FAILURES",

                        "CDEF:scaledobs=establishedtcpconn,8,*", #los valores obsevados, los multiplico *8
                        "CDEF:upper=pred,dev,2,*,+",#limite superior                        
                        "CDEF:lower=pred,dev,2,*,-",#limite inferior
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "CDEF:scaledpred=pred,8,*",

                        "LINE1:scaledobs#00FF00:Conexiones TCP establecidas",
                        "TICK:fail#FDD017:1.0:  Fallas",
                        "LINE1:scaledpred#FF00FF:Prediccion",
						"LINE1:scaledupper#00e4ef:Upper Bound Average connections",
                        "LINE1:scaledlower#ff0000:Lower Bound Average connections")
    		time.sleep(1)

	elif id_grafica == 3:
		while 1:
			print cadena
			ret = rrdtool.graph(image_name,
                        "--start", str(rrdtool.last(rrd)-1800),#'1479434100',
                        "--end",str(rrdtool.last(rrd)),
                        "--vertical-label=TCP Segs/s",
                        #Declaro cada valor que quiero mostrar en grafica
						"DEF:intcpsegs="+rrd+":intcpsegs:AVERAGE",
				        "DEF:outtcpsegs="+rrd+":outtcpsegs:AVERAGE",
                        "DEF:pred="+rrd+":intcpsegs:HWPREDICT",
                        "DEF:dev="+rrd+":intcpsegs:DEVPREDICT",
                        "DEF:fail="+rrd+":intcpsegs:FAILURES",

                        "CDEF:scaledobs=intcpsegs,8,*", #los valores obsevados, los multiplico *8
                        "CDEF:upper=pred,dev,2,*,+",#limite superior                        
                        "CDEF:lower=pred,dev,2,*,-",#limite inferior
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "CDEF:scaledpred=pred,8,*",

                        "LINE1:intcpsegs#00FF00:In TCP traffic",
                        "LINE1:outtcpsegs#0000FF:Out TCP traffic",
                        "TICK:fail#FDD017:1.0:  Fallas",
                        "LINE1:scaledpred#FF00FF:Prediccion",
						"LINE1:scaledupper#00e4ef:Upper Bound Average s. out",
                        "LINE1:scaledlower#ff0000:Lower Bound Average s. out")
			time.sleep(1)
	elif id_grafica == 4:
		while 1:
			print cadena
			ret = rrdtool.graph(image_name,
                        "--start", str(rrdtool.last(rrd)-1800),#'1479434100',
                        "--end",str(rrdtool.last(rrd)),
                        "--vertical-label=ICMP msgs/s",
                        #Declaro cada valor que quiero mostrar en grafica
						"DEF:inicmpmsgs="+rrd+":inicmpmsgs:AVERAGE",
				        "DEF:outicmpmsgs="+rrd+":outicmpmsgs:AVERAGE",
                        "DEF:pred="+rrd+":inicmpmsgs:HWPREDICT",
                        "DEF:dev="+rrd+":inicmpmsgs:DEVPREDICT",
                        "DEF:fail="+rrd+":inicmpmsgs:FAILURES",

                        "CDEF:scaledobs=inicmpmsgs,8,*", #los valores obsevados, los multiplico *8
                        "CDEF:upper=pred,dev,2,*,+",#limite superior                        
                        "CDEF:lower=pred,dev,2,*,-",#limite inferior
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "CDEF:scaledpred=pred,8,*",

                        "LINE1:scaledobs#00FF00:In ICMP msgs",
                        "LINE1:outicmpmsgs#0000FF:Out ICMP msgs",
                        "TICK:fail#FDD017:1.0:  Fallas",
                        "LINE1:scaledpred#FF00FF:Prediccion",
						"LINE1:scaledupper#00e4ef:Upper Bound Average out msgs.",
                        "LINE1:scaledlower#ff0000:Lower Bound Average out msgs.")
    		time.sleep(1)
			
	elif id_grafica == 5:
		while 1:
			print cadena
			ret = rrdtool.graph(image_name,
                        "--start", str(rrdtool.last(rrd)-1800),#'1479434100',
                        "--end",str(rrdtool.last(rrd)),
                        "--vertical-label=SNMP PDUs/s",
                        #Declaro cada valor que quiero mostrar en grafica
						"DEF:insnmpresponses="+rrd+":insnmpresponses:AVERAGE",
				        "DEF:outsnmpresponses="+rrd+":outsnmpresponses:AVERAGE",
                        "DEF:pred="+rrd+":insnmpresponses:HWPREDICT",
                        "DEF:dev="+rrd+":insnmpresponses:DEVPREDICT",
                        "DEF:fail="+rrd+":insnmpresponses:FAILURES",

                        "CDEF:scaledobs=insnmpresponses,8,*", #los valores obsevados, los multiplico *8
                        "CDEF:upper=pred,dev,2,*,+",#limite superior                        
                        "CDEF:lower=pred,dev,2,*,-",#limite inferior
                        "CDEF:scaledupper=upper,8,*",
                        "CDEF:scaledlower=lower,8,*",
                        "CDEF:scaledpred=pred,8,*",
						
                        "LINE1:scaledobs#00FF00:Solicitudes",
                        "LINE1:outsnmpresponses#0000FF:Respuestas",
                        "TICK:fail#FDD017:1.0:  Fallas",
                        "LINE1:scaledpred#FF00FF:Prediccion",
						"LINE1:scaledupper#00e4ef:Upper Bound Average respuestas",
                        "LINE1:scaledlower#ff0000:Lower Bound Average respuestas")
    		time.sleep(1)
	else:
		print "Error en la graficacion"""
		
def graficar_LB(cadena,rrd,image_name,id_grafica,limites):
	if id_grafica == 2:
		while 1:
			print cadena
			ret = rrdtool.graphv(image_name,
				"--title","Uso de RAM",
				"--start",str(tiempo_inicial),
				"--end",str(tiempo_final),
				"--vertical-label=Uso %",
				'--lower-limit', '0',
				'--upper-limit', '100',
				"DEF:ramused="+rrd+":ramused:AVERAGE",
				"CDEF:ramA=ramused,1,*", # Ajuste de escala
				"CDEF:ramU1=ramA,"+str(limites[0])+",GT,0,ramA,IF", #Si ramA es mayor que el primer umbral regresa 0, si no regresa ramA
				"VDEF:ramMAX=ramA,MAXIMUM", # Toma el maximo valor entre todos los datos de ramA
				"VDEF:ramMIN=ramA,MINIMUM", # Toma el minimo valor entre todos los datos de ramA
				"VDEF:ramSTDEV=ramA,STDEV", # Toma la desviacion estandar de todos los datos de ramA
				"VDEF:ramLAST=ramA,LAST", # Toma el ultimo valor existente en los datos de ramA
				"AREA:ramA#00FF00:Uso de RAM", # Dibuja a ram con verde
				"AREA:ramU1#FF9F00:Uso de RAM menor al "+str(limites[0])+"%", # Dibuja el trafico menor al primer umbral
				"HRULE:"+str(limites[0])+"#088A08:Umbral 1 "+str(limites[0])+"%", # Dibuja un umbral
				"HRULE:"+str(limites[1])+"#B18904:Umbral 2 "+str(limites[1])+"%", # Dibuja un umbral
				"HRULE:"+str(limites[2])+"#FF0000:Umbral 3 "+str(limites[2])+"%", # Dibuja un umbral
				"GPRINT:ramMAX:%6.2lf %SMAX", # Etiqueta
				"GPRINT:ramMIN:%6.2lf %SMIN", # Etiqueta
				"GPRINT:ramSTDEV:%6.2lf %SSTDEV", # Etiqueta
				"GPRINT:ramLAST:%6.2lf %SLAST" ) # Etiqueta
			time.sleep(1)
	else:
		print "Error en la graficacion"		


if __name__ == '__main__':
	graficar("Graficando...")
