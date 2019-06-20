#!/usr/bin/env python3

access_template = [
    'switchport mode access', 'switchport access vlan {}',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

trunk_template = [
    'switchport trunk encapsulation dot1q', 'switchport mode trunk',
    'switchport trunk allowed vlan {}'
]

port_temp = dict(access=access_template, trunk=trunk_template)
port_temp_inp = dict(access='Введите номер VLAN:', trunk='Введите разрешенные VLANы:')

mode = input('Введите режим работы интерфейса (access/trunk): ')
port = input('Введите тип и номер интерфейса: ')
vlans = input(port_temp_inp[mode])

print('interface {}'.format(port))
print('\n'.join(port_temp[mode]).format(vlans))
