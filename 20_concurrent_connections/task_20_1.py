#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 20.1

Создать функцию ping_ip_addresses, которая проверяет доступность IP-адресов.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.
'''

import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.safe_load(f)
    return devs


def ping_ip_addresses(ip_list):
    reply = subprocess.run(['ping', '-c', '2', '-W', '1', '-i', '0.2', '-n', ip_list],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8')
    if reply.returncode == 0:
        return (ip_list, True)
    else:
        return (ip_list, False)


def threads_conn(function, devices, limit=3):
    reachable = []
    unreachable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future = [executor.submit(function, device)
                for device in devices]
        for f in as_completed(future):
            if f.result()[1] is True:
                reachable.append(f.result()[0])
            else:
                unreachable.append(f.result()[0])
    return (reachable, unreachable)


if __name__ == '__main__':
    ip_list = []
    for DEVICE_PARAMS in devices('devices.yaml'):
        ip_list.append(DEVICE_PARAMS['ip'])
    print(threads_conn(ping_ip_addresses, ip_list))
