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
