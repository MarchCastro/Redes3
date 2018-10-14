import time
import rrdtool
import crearRRD
from getSNMP import consultaSNMP
from pathlib2 import Path


'''
Este script importa la funcion consultaSNMP de getSNMP y la ejecuta. Genera un valor con
las respuestas y actualiza la base de datos creada con rrd1.py.
Finalemente genera un respaldo en xml. Esto lo hace cada segundo.
'''

def actualizar(cadena,comunidad,host,puerto,rrd):
	total_input_traffic = 0
	total_output_traffic = 0
	
	#Verifica que exista una rrd asociada al host, en caso de no existir crea una rrd nueva
	archivo_rrd = Path(rrd+".rrd")
	if archivo_rrd.is_file() == False:
		crearRRD.crear(rrd+".rrd")
		print "rrd creada"
	else:
		print "Abriendo rrd..."

	#Inicia proceso de adquisicion de datos
	while 1:
		print cadena
		#octetos de entrada de la interfaz eth
		total_input_traffic = int(
			consultaSNMP(comunidad,host,puerto,
						 '1.3.6.1.2.1.2.2.1.10.2'))
	 	#octetos de salida de la interfaz eth
		total_output_traffic = int(
		    consultaSNMP(comunidad,host,puerto,
		                 '1.3.6.1.2.1.2.2.1.16.2'))
		#----------------------------------------------
	 	#numero de conexiones tcp establecidas
		total_tcp_established = int(
		    consultaSNMP(comunidad,host,puerto,
		                 '1.3.6.1.2.1.6.9.0'))
		#----------------------------------------------
		#segmentos tcp de entrada
		input_tcp_segs = int(
			consultaSNMP(comunidad,host,puerto,
						 '1.3.6.1.2.1.6.10.0'))
	 	#segmentos tcp de salida
		output_tcp_segs = int(
		    consultaSNMP(comunidad,host,puerto,
		                 '1.3.6.1.2.1.6.11.0'))
		#----------------------------------------------
		#segmentos tcp de entrada
		input_icmp_msgs = int(
			consultaSNMP(comunidad,host,puerto,
						 '1.3.6.1.2.1.5.1.0'))
	 	#segmentos tcp de salida
		output_icmp_msgs = int(
		    consultaSNMP(comunidad,host,puerto,
		                 '1.3.6.1.2.1.5.14.0'))
		#----------------------------------------------
	 	#PDUs de tipo Get-Requests generados - solicitudes generadas
		input_snmp_getReq = int(
		    consultaSNMP(comunidad,host,puerto,
		                 '1.3.6.1.2.1.11.15.0'))		
		#PDUs de tipo Get-Response generados - respuestas generadas
		output_snmp_getResp = int(
			consultaSNMP(comunidad,host,puerto,
						 '1.3.6.1.2.1.11.28.0'))

		valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic) + ':' + str(total_tcp_established) + ':' + str(input_tcp_segs) + ':' + str(output_tcp_segs) + ':' + str(input_icmp_msgs) + ':' + str(output_icmp_msgs) + ':' + str(input_snmp_getReq) + ':' + str(output_snmp_getResp)

		print valor
		rrdtool.update(rrd+'.rrd', valor) # actualizamos el archivo previamente creado en rrd1.py
		rrdtool.dump(rrd+'.rrd',rrd+'.xml') # ver el contenido de la bd opcional
		time.sleep(1)

	if ret:
		print rrdtool.error()
		time.sleep(300)

def actualizarHW(cadena,comunidad,host,puerto,rrd):
	total_input_traffic = 0
	total_output_traffic = 0
	
	#Verifica que exista una rrd asociada al host, en caso de no existir crea una rrd nueva
	archivo_rrd = Path(rrd+".rrd")
	if archivo_rrd.is_file() == False:
		crearRRD.crearHW(rrd+".rrd")
		print "rrd HW Creada..."
	else:
		print "Abriendo rrd HW..."

	#Inicia proceso de adquisicion de datos HW
	while 1:		
		total_input_traffic = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.2.2.1.10.3'))
		total_output_traffic = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.2.2.1.16.3'))

		total_tcp_established = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.6.9.0'))
		
		input_tcp_segs = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.6.10.0'))
		output_tcp_segs = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.6.11.0'))

		input_icmp_msgs = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.5.1.0'))	 	
		output_icmp_msgs = int( consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.5.14.0'))
		
		input_snmp_getReq = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.11.15.0'))
		output_snmp_getResp = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.11.28.0'))

		valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic) + ':' + str(total_tcp_established) + ':' + str(input_tcp_segs) + ':' + str(output_tcp_segs) + ':' + str(input_icmp_msgs) + ':' + str(output_icmp_msgs) + ':' + str(input_snmp_getReq) + ':' + str(output_snmp_getResp)

		#valor = str(rrdtool.last(rrd+".rrd")+60)+":" + str(total_input_traffic) + ':' + str(total_output_traffic)
		#valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
		print valor
		
		rrdtool.update(rrd+'.rrd', valor)
		rrdtool.dump(rrd+'.rrd',rrd+'.xml')
    	time.sleep(1)

	if ret:
		print rrdtool.error()
		time.sleep(300)
		
		
if __name__ == '__main__':
	actualizar("Actualizando...")
