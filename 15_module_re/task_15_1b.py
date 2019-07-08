#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них (второй).

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким образом, чтобы она возвращала список кортежей для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет несколько кортежей.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''

import re


def get_ip_from_cfg(filename):
    regex_int = r'^interface (?P<int>\S+$)'
    regex_ip = r' ip address (?P<ip>\S+) (?P<mask>\S+)'
    interfaces = {}
    with open(filename, 'r') as f:
        for string in f:
            match_int = re.search(regex_int, string)
            match_ip = re.search(regex_ip, string)
            if match_int:
                iface = match_int.group(1)
                ip_mask = []
            if match_ip:
                ip_mask.append(match_ip.groups())
                interfaces.update({iface: ip_mask})
    return interfaces


if __name__ == '__main__':
    print(get_ip_from_cfg('config_r2.txt'))