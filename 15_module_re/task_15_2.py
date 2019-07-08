#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

'''
import re


def parse_sh_ip_int_br(filename):
    regex = r'^(?P<int>\S+)\s+(?P<ip>\S+)\s+\w+\s+\w+\s+(?P<status>administratively down|up|down)\s+(?P<protocol>up|down)'
    interfaces = []
    with open(filename, 'r') as f:
        for string in f:
            match = re.search(regex, string)
            if match:
                interfaces.append(match.groups())
    return interfaces


if __name__ == '__main__':
    print(parse_sh_ip_int_br('sh_ip_int_br.txt'))
