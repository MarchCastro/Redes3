"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.snmplabs.com:161
  * for two instances of SNMPv2-MIB::sysDescr.0 MIB object,

Functionally similar to:

| $ snmpget -v1 -c public demo.snmplabs.com SNMPv2-MIB::sysDescr.0

"""#
"""from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('comunidad3', mpModel=0),
           UdpTransportTarget(('192.168.1.64', 161)),
           ContextData(),
           #ObjectType(ObjectIdentity('1.3.6.1.2.1.2.1.0')))
           ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2.2')))
           #ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.8.1')))
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
"""
from pysnmp.hlapi import *

resultado_final = ''
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
            resultado= varB.split()
            concat = []
            valid = False

            for palabra in resultado: 
                if palabra == '=':
                    valid = True
                    continue 
                    
                if valid:
                    concat.append(palabra)
            global resultado_final
            resultado_final = ''
            for palabra in concat:
                resultado_final = resultado_final + ' ' + palabra
    return resultado_final


while 1: #Monitorizamos los valores de entrada y salida de octetos de informacion
    host = 'comunidad3'
    ip = '192.168.1.64'
    total_input_traffic = consultaSNMP(host,ip,
                    '1.3.6.1.2.1.2.2.1.2.2')
    parolaHex = ''
    if total_input_traffic.startswith('0'):
				parolaHex = int('0xfff',16)
    valor = parolaHex 
    print total_input_traffic.strip().decode('hex')