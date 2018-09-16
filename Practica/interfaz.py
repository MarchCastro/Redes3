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

"""#
from pysnmp.hlapi import *

def consultaSNMP(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)),
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

total_input_traffic = 0
total_output_traffic = 0


while 1: #Monitorizamos los valores de entrada y salida de octetos de informacion
    total_input_traffic = int(
        consultaSNMP('comunidadMarcela','localhost',
                     '1.3.6.1.2.1.2.2.1.10.1'))
    total_output_traffic = int(
        consultaSNMP('comunidadMarcela','localhost',
                     '1.3.6.1.2.1.2.2.1.16.1'))

    valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
    print valor