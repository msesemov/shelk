#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from datetime import datetime
#import time
import re
from pysnmp.entity.rfc3413.oneliner import cmdgen


community = 'sbrf'
host = '192.168.100.1'
OID = {'sysinfo': '1.3.6.1.2.1.1.1.0',
       'sysname': '1.3.6.1.2.1.1.5.0',
       'location': '1.3.6.1.2.1.1.6.0'}
OID_walk = {'cdp': {'intf': '1.3.6.1.4.1.9.9.23.1.1.1.1.6',
                    'nbr': '1.3.6.1.4.1.9.9.23.1.2.1.1.6',
                    'nbr_intf': '1.3.6.1.4.1.9.9.23.1.2.1.1.7',
                    'nbr_model': '1.3.6.1.4.1.9.9.23.1.2.1.1.8'}


            }


def snmpget(host, oid, community='sbrf'):

    cmdGen = cmdgen.CommandGenerator()

    if isinstance(oid, dict):
        oid_list = []
        for key, val in oid.items():
            oid_list.append(val)

        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(community),
            cmdgen.UdpTransportTarget((host, 161)),
            *oid_list)
    elif isinstance(oid, str):
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
            cmdgen.CommunityData(community),
            cmdgen.UdpTransportTarget((host, 161)),
            oid)

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1] or '?'))
        else:
            result = {}
            for oid, value in varBinds:
                result.update({str(oid): str(value)})
            return result


def snmpwalk(host, oid, community='sbrf'):

    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.nextCmd(
        cmdgen.CommunityData(community),
        cmdgen.UdpTransportTarget((host, 161)),
        oid)

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1] or '?'))
        else:
            result = {}
            for items in varBinds:
                for key, value in items:
                    result.update({str(key): str(value)})
            return result


def cdp_nbr(host, community='sbrf'):
    cdp_host = snmpget(host, OID['sysname'])
    intf = snmpwalk(host, OID_walk['cdp']['intf'])
    nbr = snmpwalk(host, OID_walk['cdp']['nbr'])
    nbr_intf = snmpwalk(host, OID_walk['cdp']['nbr_intf'])
    print(cdp_host)
    for i in intf:
        print(i)
    for n in nbr:
        print(n)
    for ni in nbr_intf:
        print(ni)




'''
def threads_conn(function, devices, limit=30):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices)
        return list(f_result)
'''

if __name__ == '__main__':
    cdp_nbr(host)