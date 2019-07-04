#!/usr/bin/env python3
'''
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
'''


def get_int_vlan_map(config_filename):

    acc_int = {}
    trk_int = {}
    with open(config_filename, 'r') as f:
        for line in f:
            if line.startswith('interface'):
                intf = line.split()[-1]
            elif line.startswith(' switchport'):
                if line.startswith(' switchport access'):
                    if line.split()[-2] == 'vlan':
                        acc_vl = {intf: int(line.split()[-1])}
                        acc_int.update(acc_vl)

                elif line.startswith(' switchport trunk'):
                    if line.split()[-2] == 'vlan':
                        vlans = line.split()[-1]
                        trk_vl = {intf: [int(v) for v in vlans.split(',')]}
                        trk_int.update(trk_vl)
                elif line.startswith(' switchport mode access'):
                        acc_vl = {intf: 1}
                        acc_int.update(acc_vl)

    return acc_int, trk_int


print(get_int_vlan_map('config_sw2.txt'))
    