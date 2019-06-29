#!/usr/bin/env python3

'''
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN:
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN:
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

def get_int_vlan_map(config_filename):

#config_filename = 'config_sw1.txt'
    acc_int = {}
    trk_int = {}
    with open(config_filename, 'r') as f:
        for line in f:
            if line.startswith('interface'):
                intf = line.split()[-1]
            elif line.startswith(' switchport'):
                if line.startswith(' switchport access'):
                    if line.split()[-2] == 'vlan':
                        acc_vl = {intf : line.split()[-1]}
                        acc_int.update(acc_vl)
                elif line.startswith(' switchport trunk'):
                    if line.split()[-2] == 'vlan':
                        vlans = line.split()[-1]
                        trk_vl = {intf : vlans.split(',')}
                        trk_int.update(trk_vl)
    return acc_int, trk_int

print(get_int_vlan_map('config_sw1.txt'))

