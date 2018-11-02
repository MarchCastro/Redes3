import time
import rrdtool
import crearRRD
from correos import enviaCorreo_LB, send_alert_attached, check_aberration
from getSNMP import consultaSNMP
from getSNMP import consultaSNMPwalk
from pathlib2 import Path


'''
Este script importa la funcion consultaSNMP de getSNMP y la ejecuta. Genera un valor con
las respuestas y actualiza la base de datos creada con rrd1.py.
Finalemente genera un respaldo en xml. Esto lo hace cada segundo.
'''
#Un valor de 0 significa que no se ha sobrepasado ese limite, un valor de 1 indica que ese limite ya fue sobrepasado
estados_limites = [0,0,0]

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

def actualizarLB(cadena,comunidad,host,puerto,rrd,limites):
	ram_used = 0
	
	#Obtiene numero de nucleos
	num_cores = len(consultaSNMPwalk(comunidad,host,puerto,'1.3.6.1.2.1.25.3.3.1.2'))
	
	#Verifica que exista una rrd asociada al host, en caso de no existir crea una rrd nueva
	archivo_rrd = Path(rrd+".rrd")
	if archivo_rrd.is_file() == False:
		crearRRD.crearLB(rrd+".rrd",num_cores)
		print "rrd LB creada"
	else:
		print "Abriendo rrd LB..."

	#Obtiene max ram del host
	max_ram = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.4.1.2021.4.5.0'))
	#Obtiene max HDD del host
	max_hdd = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.25.2.3.1.5.1'))

	#Variable de insercion en rrd
	valor = ""

	#Inicia proceso de adquisicion de datos
	while 1:
		print cadena
		
		#-----------------------------------------------------------------
		#Adquisicion de RAM
		ram_used = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.4.1.2021.4.6.0')) #Memoria libre
		porcentaje = (ram_used*100)/max_ram # Porcentaje de RAM libre
		porcentaje = 100 - porcentaje; # Porcentaje de RAM usada
		valor = "N:" + str(porcentaje)

		#Verifica limites para enviar notificaciones notificaciones
		if porcentaje >= limites[2] and estados_limites[2] == 0:
			estados_limites[2] = 1
			notificar(host,comunidad,'% de RAM - umbral go',limites[2],'',str(1))
		elif porcentaje >= limites[1] and estados_limites[1] == 0:
			estados_limites[1] = 1
			notificar(host,comunidad,'% de RAM - umbral set',limites[1],'',str(1))
		elif porcentaje >= limites[0] and estados_limites[0] == 0:
			estados_limites[0] = 1
			notificar(host,comunidad,'% de RAM - umbral ready',limites[0],'',str(1))

		#-----------------------------------------------------------------
		#Adquisicion de HDD
		hdd_used = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.25.2.3.1.6.1')) #HDD usado
		porcentaje = (hdd_used*100)/max_hdd # Porcentaje de HDD usado
		valor += ":" + str(porcentaje)		
		
		#Verifica limites para enviar notificaciones notificaciones
		if porcentaje >= limites[2] and estados_limites[2] == 0:
			estados_limites[2] = 1
			notificar(host,comunidad,'% de Almacenamiento - umbral go',limites[2],'',str(2))
		elif porcentaje >= limites[1] and estados_limites[1] == 0:
			estados_limites[1] = 1
			notificar(host,comunidad,'% de Almacenamiento - umbral set',limites[1],'',str(2))
		elif porcentaje >= limites[0] and estados_limites[0] == 0:
			estados_limites[0] = 1
			notificar(host,comunidad,'% de Almacenamiento - umbral ready',limites[0],'',str(2))
		#-----------------------------------------------------------------
		#Adquisicion de CPU
		cores = consultaSNMPwalk(comunidad,host,puerto,'1.3.6.1.2.1.25.3.3.1.2')
		x = 1
		for porcentaje in cores:
			valor += ":" + porcentaje
			#Verifica limites para enviar notificaciones notificaciones
			if porcentaje >= limites[2] and estados_limites[2] == 0:
				estados_limites[2] = 1
				notificar(host,comunidad,'% de Procesamiento en nucleo '+str(x)+' - umbral go',limites[2],"-"+str(x),str(3))
			elif porcentaje >= limites[1] and estados_limites[1] == 0:
				estados_limites[1] = 1
				notificar(host,comunidad,'% de Procesamiento en nucleo '+str(x)+' - umbral set',limites[1],"-"+str(x),str(3))
			elif porcentaje >= limites[0] and estados_limites[0] == 0:
				estados_limites[0] = 1
				notificar(host,comunidad,'% de Procesamiento en nucleo '+str(x)+' - umbral ready',limites[0],"-"+str(x),str(3))
			x = x +1		
		#-----------------------------------------------------------------

		print "LB - " + valor
		rrdtool.update(rrd+'.rrd', valor) # actualizamos el archivo previamente creado en rrd1.py
		rrdtool.dump(rrd+'.rrd',rrd+'.xml') # ver el contenido de la bd opcional
		time.sleep(1)

	if ret:
		print rrdtool.error()
		time.sleep(300)


def actualizarHW(cadena,comunidad,host,puerto,rrd):
	print 'Entro actualizarHW ',cadena,comunidad,host,puerto,rrd
	
	total_input_traffic = 0
	total_output_traffic = 0
	rrdpath="./RRD_HW/"
	pngpath="./IMG_HW/"
	fname=rrd+".rrd"
	pngfname=rrd+".png"
	#Verifica que exista una rrd asociada al host, en caso de no existir crea una rrd nueva
	archivo_rrd = Path(rrdpath+fname)
	if archivo_rrd.is_file() == False:
		crearRRD.crearHW(rrdpath+fname)
		print "rrd HW Creada... en",rrdpath,fname
	else:
		print "Abriendo rrd HW..."

	endDate = rrdtool.last(rrdpath+fname) #ultimo valor del XML
	begDate = endDate - 3600
	#Inicia proceso de adquisicion de datos HW
	while 1:		
		total_input_traffic = int(consultaSNMP('public','10.100.71.100',1024,'1.3.6.1.2.1.2.2.1.18.1'))
		total_output_traffic = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.2.2.1.16.3'))
		
		'''total_tcp_established = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.6.9.0'))
		
		input_tcp_segs = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.6.10.0'))
		output_tcp_segs = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.6.11.0'))

		input_icmp_msgs = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.5.1.0'))	 	
		output_icmp_msgs = int( consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.5.14.0'))
		
		input_snmp_getReq = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.11.15.0'))
		output_snmp_getResp = int(consultaSNMP(comunidad,host,puerto,'1.3.6.1.2.1.11.28.0'))'''
		
		#valor = str(rrdtool.last(rrdpath+fname)+30) + str(total_input_traffic) + ':' + str(total_output_traffic) + ':' + str(total_tcp_established) + ':' + str(input_tcp_segs) + ':' + str(output_tcp_segs) + ':' + str(input_icmp_msgs) + ':' + str(output_icmp_msgs) + ':' + str(input_snmp_getReq) + ':' + str(output_snmp_getResp)
		
		#valor = str(rrdtool.last(rrdpath+fname)+30)+":" + str(total_input_traffic) + ':' + str(total_output_traffic) + ':' + str(total_tcp_established) + ':' + str(input_tcp_segs) + ':' + str(output_tcp_segs) + ':' + str(input_icmp_msgs) + ':' + str(output_icmp_msgs) + ':' + str(input_snmp_getReq) + ':' + str(output_snmp_getResp)
		valor = str(rrdtool.last(rrdpath+fname)+30)+":" + str(total_input_traffic)
		print 'Valor: ',valor
		rrdtool.update(rrdpath+fname,valor)
		rrdtool.dump(rrdpath+fname,rrd+'.xml')
		#print "actualizar: ",rrdpath,fname, rrd
		rrdtool.tune(rrdpath+fname,'--alpha','0.1')
		#time.sleep(1)			
	if ret:
		print rrdtool.error()
		time.sleep(300)

def notificar(host,comunidad,unidad,limite,id_nucleo,id_grafica):
	#Implementa envio de correo electronico
	cad = "Notificacion importante - mini Observium\nEl host "+host+" perteneciente a la comunidad "+comunidad+" ha sobrepasado el limite de "+str(limite)+" "+unidad+" permitida."
	#print cad + " " + host+"-"+id_grafica+"-LB.png"+id_nucleo
	enviaCorreo_LB(cad,host+"-"+id_grafica+"-LB.png"+id_nucleo)


if __name__ == '__main__':
	actualizar("Actualizando...")
