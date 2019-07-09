#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
'''

import re


def convert_ios_nat_to_asa(config_IOS, reult_config_ASA):
    regex = r'ip nat \S+ \S+ \S+ (?P<proto>\S+) (?P<ip>[\d.]+) (?P<port1>\d+) \S+ \S+ (?P<port2>\S+)'
    asa1 = 'object network LOCAL_{}\n'
    asa2 = ' host {}\n nat (inside,outside) static interface service {} {} {}\n'
    with open(config_IOS, 'r') as f, open(reult_config_ASA, 'w') as dest:
        for line in f:
            match = re.search(regex, line)
            nat1 = asa1.format(match.group('ip'))
            nat2 = asa2.format(match.group('ip'), match.group('proto'), match.group('port1'), match.group('port2'))
            dest.write(nat1)
            dest.write(nat2)

if __name__ == '__main__':
    convert_ios_nat_to_asa('cisco_nat_config.txt', 'res_asa_cfg.txt')
