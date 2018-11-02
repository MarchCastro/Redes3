"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.snmplabs.com:161
  * for two instances of SNMPv2-MIB::sysDescr.0 MIB object,

Functionally similar to:

| $ snmpget -v1 -c public localhost SNMPv2-MIB::sysDescr.0

Script que captura datos SNMP y la funcion consultaSNMP regresa el resultado de la consulta

"""#
from pysnmp.hlapi import *

def consultaSNMP(comunidad,host,puerto,oid):
	'''
		Recibe el nombre de la comunidad, el host o ip y el OID a consultar
	'''
	#resultado = ''
	errorIndication, errorStatus, errorIndex, varBinds = next(
		getCmd(SnmpEngine(),
			CommunityData(comunidad),
			UdpTransportTarget((host, puerto)),
			ContextData(),
			ObjectType(ObjectIdentity(oid))))

	if errorIndication:
		print(errorIndication)
	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
	else:
		for varBind in varBinds:
		    varB=(' = '.join([x.prettyPrint() for x in varBind]))
		    resultado= varB.split()[2]
	return resultado

def consultaSNMPwalk(comunidad,host,puerto,oid):
	'''
		Recibe el nombre de la comunidad, el host o ip y el OID a consultar
	'''
	resultado = []
	for (errorIndication,
		errorStatus,
		errorIndex,
		varBinds) in nextCmd(SnmpEngine(), 
				          CommunityData(comunidad),
				          UdpTransportTarget((host, puerto)),
				          ContextData(),                                                           
				          ObjectType(ObjectIdentity(oid)),
				          lexicographicMode=False):
		if errorIndication:
			print(errorIndication)
			break
		elif errorStatus:
			print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
			break
		else:
			for varBind in varBinds:
				varB=(' = '.join([x.prettyPrint() for x in varBind]))
				resultado.append(varB.split()[2])
	return resultado

if __name__ == '__main__':
	print consultaSNMPwalk('comunidadEquipo12_4CM3','127.0.0.1','161','1.3.6.1.2.1.25.3.3.1.2')







