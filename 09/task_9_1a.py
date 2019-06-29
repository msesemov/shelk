#!/usr/bin/env python3


access_mode_template = [
    'switchport mode access', 'switchport access vlan',
    'switchport nonegotiate', 'spanning-tree portfast',
    'spanning-tree bpduguard enable'
]

port_security_template = [
    'switchport port-security maximum 2',
    'switchport port-security violation restrict',
    'switchport port-security'
]

access_config = {
    'FastEthernet0/12': 10,
    'FastEthernet0/14': 11,
    'FastEthernet0/16': 17
}

def generate_access_config(intf_vlan_mapping, access_template, port_security=None):
    '''
    intf_vlan_mapping - словарь с соответствием интерфейс-VLAN такого вида:
         {'FastEthernet0/12':10,
         'FastEthernet0/14':11,
         'FastEthernet0/16':17}
    access_template - список команд для порта в режиме access

    Возвращает список всех портов в режиме access с конфигурацией на основе шаблона
    '''


    command = []
    for intf, vlan in intf_vlan_mapping.items():
        command.append('interface ' + intf)
        for line in access_template:
            if line.endswith('access vlan'):
                command.append(f'{line} {vlan}')
            else:
                command.append(line)
        #command.append([ps_command for ps_command in port_security if port_security]
        if port_security:
            for ps_command in port_security:
                command.append(ps_command)
    return command

print(generate_access_config(access_config, access_mode_template, port_security_template))