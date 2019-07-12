#!/usr/bin/env python3
from datetime import datetime
import time
from pysnmp import hlapi
import ipaddress
import subprocess
from concurrent.futures import ThreadPoolExecutor
import socket

start_time = datetime.now()
community = 'sbrf'
proto = 'udp'
port = 161
OID = ['1.3.6.1.2.1.1.5.0']
NETS = [#'192.168.232.0/24',
            #'192.168.240.0/24',
            #'192.168.241.0/24',
            #'192.168.244.0/24',
            #'192.168.248.0/22',
            #'192.168.252.0/24',
            #'192.168.253.0/24',
            '192.168.254.64/28']





#def get_ptr(host):


def ping_ip(ip):
    reply = subprocess.run(['ping', '-c', '1', '-W', '1', '-i', '0.2', '-n', ip],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding='utf-8')
    if reply.returncode == 0:
        return [ip ,True]
    else:
        return [ip, False]


def port_is_open(host, port, proto):
    if proto == 'udp':
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))
        if result == 0:
            s.close()
            return True
        else:
            s.close()
            return False
    elif proto == 'tcp':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))
        if result == 0:
            s.close()
            return True
        else:
            s.close()
            return False
    else:
        return 'Please specify tcp/udp protocol'


def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]


def threads_conn(function, devices, limit=20):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices)
    return list(f_result)


full_list = []
for net in NETS:
    subnet = ipaddress.ip_network(net)
    for ip in subnet:
        full_list.append(str(ip))

for s in threads_conn(ping_ip, full_list):
    if s[1] is True:
        if port_is_open(s[0], port, proto):
            print(get(s[0], OID, hlapi.CommunityData('sbrf')))
            #print(f'{s[0]}:\t{sysname}')
        else:
            print(f'{s[0]}: UPD/161 is not opened')

#print(get('192.168.254.67', OID, hlapi.CommunityData('sbrf')))
#print(socket.gethostbyaddr('192.168.253.20'))
print(datetime.now() - start_time)
