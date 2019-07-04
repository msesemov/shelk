#!/usr/bin/env python3


trunk_mode_template = [
    'switchport mode trunk', 'switchport trunk native vlan 999',
    'switchport trunk allowed vlan'
]

trunk_config = {
    'FastEthernet0/1': [10, 20, 30],
    'FastEthernet0/2': [11, 30],
    'FastEthernet0/4': [17]
}



def generate_trunk_config(intf_vlan_mapping, trunk_template):
    '''
    intf_vlan_mapping - словарь с соответствием интерфейс-VLAN такого вида:
         {'FastEthernet0/12': [10, 20],
         'FastEthernet0/14': [11, 30],
         'FastEthernet0/16': [17]}
    trunk_template - список команд для порта в режиме trunk

    Возвращает список всех портов в режиме trunk с конфигурацией на основе шаблона
    '''
#intf_vlan_mapping = trunk_config
#trunk_template = trunk_mode_template

    command = []
    for intf, vlan in intf_vlan_mapping.items():
        command.append('interface ' + intf)
        for line in trunk_template:
            if line.endswith('allowed vlan'):
                v = ','.join([str(vl) for vl in vlan])
                command.append(f'{line} {v}')
            else:
                command.append(line)
    return command

print(generate_trunk_config(trunk_config, trunk_mode_template))