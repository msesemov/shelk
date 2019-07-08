#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
'''

import re


def get_ints_without_description(filename):
    regex_int = r'^interface (?P<int>\S+$)'
    regex_desc = r' description (?P<description>.*)'
    all_ifaces = []
    desc_ifaces = []
    with open(filename, 'r') as f:
        for string in f:
            match_int = re.search(regex_int, string)
            match_desc = re.search(regex_desc, string)
            if match_int:
                iface = match_int.group(1)
                all_ifaces.append(iface)
            if match_desc:
                desc_ifaces.append(iface)
    for di in desc_ifaces:
        if di in all_ifaces:
            all_ifaces.remove(di)
    return all_ifaces


if __name__ == '__main__':
    print(get_ints_without_description('config_r1.txt'))
