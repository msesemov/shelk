#!/usr/bin/env python3

access_template = [
    'interface {}',
    'switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

trunk_template = [
    'interface {}',
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}'
]

port_temp = dict(access=access_template, trunk=trunk_template)
mode = input('Введите режим работы интерфейса (access/trunk): ')
port = input('Введите тип и номер интерфейса: ')
vlans = input('Введите номер влан(ов): ')


print('\n'.join(port_temp[mode]).format(port, vlans))
