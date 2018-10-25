import sys
import rrdtool
import time
from correos import send_alert_attached, check_aberration
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
	print "GRAFICAR ",rrd,image_name
	rrdpath="./RRD_HW/"
	pngpath="./IMG_HW/"
	title="Deteccion de comportamiento anomalo"
	var = 0
	if id_grafica == 1:	
		while 1:
			ret = rrdtool.graph(pngpath+image_name,
									'--start', str(rrdtool.last(rrdpath+rrd)-25800),
									#'--start', str(rrdtool.last(fname)-51600),
									'--end', str(rrdtool.last(rrdpath+rrd)),
									'--title=' + title,
									"--vertical-label=Bytes/s",
									'--slope-mode',
									"DEF:obs="       + rrdpath+rrd + ":inoctets:AVERAGE",
									"DEF:outoctets=" + rrdpath+rrd + ":outoctets:AVERAGE",
									"DEF:pred="      + rrdpath+rrd + ":inoctets:HWPREDICT",
									"DEF:dev="       + rrdpath+rrd + ":inoctets:DEVPREDICT",
									"DEF:fail="      + rrdpath+rrd + ":inoctets:FAILURES",

									"CDEF:scaledobs=obs,8,*",
									"CDEF:upper=pred,dev,2,*,+",
									"CDEF:lower=pred,dev,2,*,-",
									"CDEF:scaledupper=upper,8,*",
									"CDEF:scaledlower=lower,8,*",
									"CDEF:scaledpred=pred,8,*",
									
									"TICK:fail#FDD017:1.0:  Fallas",
									"LINE3:scaledobs#00FF00:In traffic",
									"LINE1:scaledpred#FF00FF:Prediccion\\n",
									#"LINE1:outoctets#0000FF:Out traffic",
									"LINE1:scaledupper#ff0000:Upper Bound Average bits in\\n",
									"LINE1:scaledlower#0000FF:Lower Bound Average bits in")
    		
			time.sleep(1)
			returned_value = check_aberration(rrdpath,rrd)
			print returned_value
			
			if var == returned_value:
				pass
			else:    
				if var == 0 and returned_value == 1 or var == 2 and returned_value == 1:
					send_alert_attached('New aberrations detected',pngpath+image_name)
					var = returned_value
				elif var == 1 and returned_value == 2:
					send_alert_attached('Abberations gone',pngpath+image_name)
					var = returned_value

	elif id_grafica == 2:	
		while 1:
			ret = rrdtool.graph(pngpath+image_name,
									'--start', str(rrdtool.last(rrdpath+rrd)-25800),
									#'--start', str(rrdtool.last(fname)-51600),
									'--end', str(rrdtool.last(rrdpath+rrd)),
									'--title=' + title,
									"--vertical-label=Numero de conexiones",
									'--slope-mode',

									"DEF:establishedtcpconn="+rrdpath+rrd+":establishedtcpconn:AVERAGE",
									"DEF:pred="+rrdpath+rrd+":establishedtcpconn:HWPREDICT",
									"DEF:dev="+rrdpath+rrd+":establishedtcpconn:DEVPREDICT",
									"DEF:fail="+rrdpath+rrd+":establishedtcpconn:FAILURES",

									"CDEF:scaledobs=establishedtcpconn,8,*", #los valores obsevados, los multiplico *8
									"CDEF:upper=pred,dev,2,*,+",#limite superior                        
									"CDEF:lower=pred,dev,2,*,-",#limite inferior
									"CDEF:scaledupper=upper,8,*",
									"CDEF:scaledlower=lower,8,*",
									"CDEF:scaledpred=pred,8,*",
									
									"TICK:fail#FDD017:1.0:  Fallas",
									"LINE3:scaledobs#00FF00:Conexiones TCP establecidas",								
									"LINE1:scaledpred#FF00FF:Prediccion\\n",
									"LINE1:scaledupper#ff0000:Upper Bound Average connections\\n",
									"LINE1:scaledlower#0000FF:Lower Bound Average connections")
    		
			time.sleep(1)
			returned_value = check_aberration(rrdpath,rrd)
			print returned_value
			
			if var == returned_value:
				pass
			else:    
				if var == 0 and returned_value == 1 or var == 2 and returned_value == 1:
					send_alert_attached('New aberrations detected',pngpath+image_name)
					var = returned_value
				elif var == 1 and returned_value == 2:
					send_alert_attached('Abberations gone',pngpath+image_name)
					var = returned_value

	elif id_grafica == 3:
		while 1:
			ret = rrdtool.graph(pngpath+image_name,
									'--start', str(rrdtool.last(rrdpath+rrd)-25800),
									#'--start', str(rrdtool.last(fname)-51600),
									'--end', str(rrdtool.last(rrdpath+rrd)),
									'--title=' + title,
									"--vertical-label=TCP Segs/s",
									'--slope-mode',								

									"DEF:intcpsegs="+rrdpath+rrd+":intcpsegs:AVERAGE",
									"DEF:outtcpsegs="+rrdpath+rrd+":outtcpsegs:AVERAGE",
									"DEF:pred="+rrdpath+rrd+":intcpsegs:HWPREDICT",
									"DEF:dev="+rrdpath+rrd+":intcpsegs:DEVPREDICT",
									"DEF:fail="+rrdpath+rrd+":intcpsegs:FAILURES",
									
									"CDEF:scaledobs=intcpsegs,8,*", #los valores obsevados, los multiplico *8
									"CDEF:upper=pred,dev,2,*,+",#limite superior                        
									"CDEF:lower=pred,dev,2,*,-",#limite inferior
									"CDEF:scaledupper=upper,8,*",
									"CDEF:scaledlower=lower,8,*",
									"CDEF:scaledpred=pred,8,*",

									"TICK:fail#FDD017:1.0:  Fallas",
									"LINE3:intcpsegs#00FF00:In TCP traffic",
									#"LINE1:outtcpsegs#0000FF:Out TCP traffic",
									"LINE1:scaledpred#FF00FF:Prediccion\\n",
									#"LINE1:outoctets#0000FF:Out traffic",
									"LINE1:scaledupper#ff0000:Upper Bound Average s. in\\n",
									"LINE1:scaledlower#0000FF:Lower Bound Average s. in")
    		
			time.sleep(1)
			returned_value = check_aberration(rrdpath,rrd)
			print returned_value
			
			if var == returned_value:
				pass
			else:    
				if var == 0 and returned_value == 1 or var == 2 and returned_value == 1:
					send_alert_attached('New aberrations detected',pngpath+image_name)
					var = returned_value
				elif var == 1 and returned_value == 2:
					send_alert_attached('Abberations gone',pngpath+image_name)
					var = returned_value

	elif id_grafica == 4:
		while 1:
			ret = rrdtool.graph(pngpath+image_name,
									'--start', str(rrdtool.last(rrdpath+rrd)-25800),
									#'--start', str(rrdtool.last(fname)-51600),
									'--end', str(rrdtool.last(rrdpath+rrd)),
									'--title=' + title,
									"--vertical-label=ICMP msgs/s",
									'--slope-mode',
									
									"DEF:inicmpmsgs="+rrdpath+rrd+":inicmpmsgs:AVERAGE",
									"DEF:outicmpmsgs="+rrdpath+rrd+":outicmpmsgs:AVERAGE",
									"DEF:pred="+rrdpath+rrd+":inicmpmsgs:HWPREDICT",
									"DEF:dev="+rrdpath+rrd+":inicmpmsgs:DEVPREDICT",
									"DEF:fail="+rrdpath+rrd+":inicmpmsgs:FAILURES",
									
									"CDEF:scaledobs=inicmpmsgs,8,*", #los valores obsevados, los multiplico *8
									"CDEF:upper=pred,dev,2,*,+",#limite superior                        
									"CDEF:lower=pred,dev,2,*,-",#limite inferior
									"CDEF:scaledupper=upper,8,*",
									"CDEF:scaledlower=lower,8,*",
									"CDEF:scaledpred=pred,8,*",

									"TICK:fail#FDD017:1.0:  Fallas",
									"LINE3:scaledobs#00FF00:In ICMP msgs",
                        			#"LINE3:outicmpmsgs#0000FF:Out ICMP msgs",
									"LINE1:scaledpred#FF00FF:Prediccion\\n",
									#"LINE1:outoctets#0000FF:Out traffic",
									"LINE1:scaledupper#ff0000:Upper Bound Average in msgs.\\n",
									"LINE1:scaledlower#0000FF:Lower Bound Average in msgs.")
			time.sleep(1)
			returned_value = check_aberration(rrdpath,rrd)
			print returned_value
			
			if var == returned_value:
				pass
			else:    
				if var == 0 and returned_value == 1 or var == 2 and returned_value == 1:
					send_alert_attached('New aberrations detected',pngpath+image_name)
					var = returned_value
				elif var == 1 and returned_value == 2:
					send_alert_attached('Abberations gone',pngpath+image_name)
					var = returned_value
			
	elif id_grafica == 5:
		while 1:
			ret = rrdtool.graph(pngpath+image_name,
									'--start', str(rrdtool.last(rrdpath+rrd)-25800),
									#'--start', str(rrdtool.last(fname)-51600),
									'--end', str(rrdtool.last(rrdpath+rrd)),
									'--title=' + title,
									"--vertical-label=SNMP PDUs/s",
									'--slope-mode',
									
									"DEF:insnmpresponses="+rrdpath+rrd+":insnmpresponses:AVERAGE",
									"DEF:outsnmpresponses="+rrdpath+rrd+":outsnmpresponses:AVERAGE",
									"DEF:pred="+rrdpath+rrd+":insnmpresponses:HWPREDICT",
									"DEF:dev="+rrdpath+rrd+":insnmpresponses:DEVPREDICT",
									"DEF:fail="+rrdpath+rrd+":insnmpresponses:FAILURES",

									"CDEF:scaledobs=insnmpresponses,8,*", #los valores obsevados, los multiplico *8
									"CDEF:upper=pred,dev,2,*,+",#limite superior                        
									"CDEF:lower=pred,dev,2,*,-",#limite inferior
									"CDEF:scaledupper=upper,8,*",
									"CDEF:scaledlower=lower,8,*",
									"CDEF:scaledpred=pred,8,*",

									"TICK:fail#FDD017:1.0:  Fallas",
									"LINE3:scaledobs#00FF00:Solicitudes",
									#"LINE1:outsnmpresponses#0000FF:Respuestas",
									"LINE1:scaledpred#FF00FF:Prediccion\\n",
									#"LINE1:outoctets#0000FF:Out traffic",
									"LINE1:scaledupper#ff0000:Upper Bound Average in responses\\n",
									"LINE1:scaledlower#0000FF:Lower Bound Average in responses")
    		
			time.sleep(1)
			returned_value = check_aberration(rrdpath,rrd)
			print returned_value
			
			if var == returned_value:
				pass
			else:    
				if var == 0 and returned_value == 1 or var == 2 and returned_value == 1:
					send_alert_attached('New aberrations detected',pngpath+image_name)
					var = returned_value
				elif var == 1 and returned_value == 2:
					send_alert_attached('Abberations gone',pngpath+image_name)
					var = returned_value
	else:
		print "Error en la graficacion"
		
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
