#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
'''

import subprocess


def ping_ip_addresses(ip_list):
    alive = []
    unreachable = []
    for ip in ip_list:
        reply = subprocess.run(['ping', '-c', '2', '-W', '1', '-i', '0.2', '-n', ip],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    encoding='utf-8')
        if reply.returncode == 0:
            alive.append(ip)
        else:
            unreachable.append(ip)
    result = (alive, unreachable)
    return result


if __name__ == '__main__':
    ip_list = ['8.8.8.8', '4.4.4.4', '1.1.1.1', '123.324.41.12', '123.2.3.3']
    print(ping_ip_addresses(ip_list))
