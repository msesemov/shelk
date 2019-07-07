#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 12.2


Функция check_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона, например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список, где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список IP-адресов и/или диапазонов IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только последний октет адреса.

Функция возвращает список IP-адресов.


Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

'''

import ipaddress


def convert_ranges_to_ip_list(ip_list):
    result = []
    for ip in ip_list:
        ip = ip.split('-')
        if len(ip) > 1 and ip[1].isdigit():
            s_ip = ip[0].split()
            start_ipv4 = ipaddress.ip_address(ip[0])
            end_ipv4 = ipaddress.ip_address(f'{s_ip[0][:-1]}{ip[1]}')
            for i in range(int(start_ipv4), int(end_ipv4) + 1):
                result.append(str(ipaddress.ip_address(i)))
        elif len(ip) > 1 and ip[1]:
            start_ipv4 = ipaddress.ip_address(ip[0])
            end_ipv4 = ipaddress.ip_address(ip[1])
            for i in range(int(start_ipv4), int(end_ipv4) + 1):
                result.append(str(ipaddress.ip_address(i)))
        else:
            ipv4 = ipaddress.ip_address(ip[0])
            result.append(str(ipv4))

    return result



if __name__ == '__main__':
    ip_list = ['8.8.8.8', '4.4.4.4-6', '123.24.41.254-123.24.42.2']
    print(convert_ranges_to_ip_list(ip_list))
