#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов, а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
'''
import re


def generate_description_from_cdp(filename):
    descr = {}
    regex = r'(\S+)\s+(\S+ \d+/\d+)\s+.*\s+(\S+ \d+/\d+)'
    with open(filename, 'r') as f:
        for string in f:
            m = re.match(regex, string)
            if m:
                d = re.sub(regex, r'description Connected to \1 port \3', string)
                descr.update({m.group(2): d.strip()})
    return descr


if __name__ == '__main__':
    print(generate_description_from_cdp('sh_cdp_n_sw1.txt'))
