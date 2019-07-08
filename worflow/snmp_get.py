#!/usr/bin/env python3

from pysnmp.hlapi import *

community = 'sbrf'
host = '192.168.251.186'
port = 161
OID = '1.3.6.1.2.1.1.5.0'

def snmp_get(community, host, port, OID):
    iterator = getCmd(SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity(OID)))

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
        else:
            for varBind in varBinds:
                #print (' = '.join([x.prettyPrint() for x in varBind]))
                return varBind[1]

print(snmp_get(community, host, port, OID))