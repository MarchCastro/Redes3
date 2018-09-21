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
'''
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
                    '1.3.6.1.2.1.1.1.0')

    valor = "N:" + total_input_traffic 
    print valor'''

import PIL
from PIL import Image
img = Image.open('linux.png').convert('L')
img.show()
img.save('brick-house-gs','png')