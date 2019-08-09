#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Задание 20.3

Создать функцию send_command_to_devices, которая отправляет
разные команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
'''

import netmiko
import paramiko
from concurrent.futures import ThreadPoolExecutor, as_completed


def devices(src_yaml):
    import yaml
    with open(src_yaml, 'r') as f:
        devs = yaml.safe_load(f)
    return devs


def send_show_command_to_devices(devices, commands_dict, filename, limit=3):
    with open(filename, 'w+') as wfile:
        with ThreadPoolExecutor(max_workers=limit) as executor:
            future = [executor.submit(send_show_command, device, commands_dict[device['ip']])
                    for device in devices]
            for f in as_completed(future):
                    wfile.write(f.result())


def send_show_command(DEVICE_PARAMS, COMMAND):
    try:
        with netmiko.ConnectHandler(**DEVICE_PARAMS) as ssh:
            ssh.enable()
            prompt = '\n' + ssh.find_prompt() + COMMAND + '\n'
            result = prompt  + ssh.send_command(COMMAND)
            return result
    except paramiko.ssh_exception.AuthenticationException as e:
        return e
    except netmiko.ssh_exception.NetMikoTimeoutException as e:
        return e


if __name__ == '__main__':
    commands = {'192.168.100.1': 'sh ip int br',
                '192.168.100.2': 'sh arp',
                '192.168.100.3': 'sh ip int br'}
    send_show_command_to_devices(devices('devices.yaml'), commands, 'output.txt')
