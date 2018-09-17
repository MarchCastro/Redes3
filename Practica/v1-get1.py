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
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('comunidadMarcela', mpModel=0),
           UdpTransportTarget(('localhost', 161)),
           ContextData(),
           #ObjectType(ObjectIdentity('1.3.6.1.2.1.2.1.0')))
           ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2.3')))
           #ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.8.3')))
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
