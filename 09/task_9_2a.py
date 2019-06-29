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

    int_cfg = {key: [] for key in intf_vlan_mapping}
    for intf, vlan in intf_vlan_mapping.items():
        for line in trunk_template:
            if line.endswith('allowed vlan'):
                v = ','.join([str(vl) for vl in vlan])
                int_cfg[intf].append(f'{line} {v}')
                
            else:
                int_cfg[intf].append(line)
    return int_cfg

print(generate_trunk_config(trunk_config, trunk_mode_template))